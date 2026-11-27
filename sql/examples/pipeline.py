"""DataHarbor: single-host ordered batch log, atomic DB checkpoint and recoverable publication.

This synthetic source uses dense integer sequences. Real PostgreSQL LSNs are opaque;
they are not incremented here and no broker or replication slot is simulated as live.
"""
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
import hashlib,json,os,uuid
from fixtures import connect
from contracts import utc

MODEL_VERSION='dataharbor-v1'

def canonical(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(value):return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()
def file_digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def atomic_json(path,value):
    path=Path(path);temporary=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    with temporary.open('x',encoding='utf-8') as stream:
        stream.write(canonical(value)+'\n');stream.flush();os.fsync(stream.fileno())
    os.replace(temporary,path)

@contextmanager
def writer_lock(workspace):
    workspace=Path(workspace).resolve();workspace.mkdir(parents=True,exist_ok=True)
    lock=workspace/'writer.lock'
    try:descriptor=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError:raise RuntimeError('Workspace writer lock exists; inspect ownership before recovery') from None
    try:
        os.write(descriptor,str(os.getpid()).encode('ascii'));os.close(descriptor);descriptor=None
        yield
    finally:
        if descriptor is not None:os.close(descriptor)
        lock.unlink()

def validate_batch(batch):
    if not isinstance(batch,dict) or set(batch)!={'batch_id','after_seq','through_seq','events'}:raise ValueError('Invalid batch envelope')
    name=batch['batch_id'];lo=batch['after_seq'];hi=batch['through_seq'];events=batch['events']
    if not isinstance(name,str) or not name or len(name)>80:raise ValueError('Invalid batch id')
    if type(lo) is not int or type(hi) is not int or lo<0 or hi<lo:raise ValueError('Invalid sequence bounds')
    if not isinstance(events,list) or len(events)>10000 or hi-lo>10000:raise ValueError('Invalid batch size')
    unique={}
    fields={'event_id','seq','op','order_id','customer_id','ordered_at','event_at','status','amount_cents'}
    for event in events:
        if not isinstance(event,dict) or set(event)!=fields:raise ValueError('Invalid event schema')
        if not isinstance(event['event_id'],str) or not event['event_id'] or len(event['event_id'])>80:raise ValueError('Invalid event id')
        for key in ('seq','order_id','customer_id','amount_cents'):
            if type(event[key]) is not int or event[key]<0:raise ValueError('Invalid integer field: '+key)
        if event['order_id']==0 or event['customer_id']==0:raise ValueError('Positive business keys required')
        if event['op'] not in ('upsert','delete') or event['status'] not in ('paid','cancelled'):raise ValueError('Invalid operation or status')
        if not isinstance(event['ordered_at'],str) or not isinstance(event['event_at'],str):raise ValueError('Timestamp string required')
        utc(event['ordered_at']);utc(event['event_at'])
        old=unique.get(event['event_id'])
        if old is not None and old!=event:raise ValueError('Conflicting duplicate event id')
        unique[event['event_id']]=dict(event)
    ordered=sorted(unique.values(),key=lambda event:event['seq'])
    if [e['seq'] for e in ordered]!=list(range(lo+1,hi+1)):raise ValueError('Synthetic source range is incomplete or ambiguous')
    return ordered

def initialize(connection):
    connection.execute('''
CREATE TABLE IF NOT EXISTS cursor_state(singleton INTEGER PRIMARY KEY CHECK(singleton=1),last_seq BIGINT NOT NULL);
INSERT INTO cursor_state VALUES(1,0) ON CONFLICT DO NOTHING;
CREATE TABLE IF NOT EXISTS raw_events(event_id VARCHAR PRIMARY KEY,seq BIGINT UNIQUE NOT NULL,payload_hash VARCHAR NOT NULL,payload VARCHAR NOT NULL);
CREATE TABLE IF NOT EXISTS order_state(order_id BIGINT PRIMARY KEY,customer_id BIGINT NOT NULL,ordered_at TIMESTAMPTZ NOT NULL,
 status VARCHAR NOT NULL,amount_cents BIGINT NOT NULL CHECK(amount_cents>=0),source_seq BIGINT NOT NULL,deleted BOOLEAN NOT NULL);
CREATE TABLE IF NOT EXISTS publication_outbox(batch_id VARCHAR PRIMARY KEY,payload_hash VARCHAR NOT NULL,through_seq BIGINT NOT NULL,version_id VARCHAR NOT NULL,published BOOLEAN NOT NULL);
CREATE OR REPLACE VIEW live_orders AS SELECT order_id,customer_id,ordered_at,status,amount_cents,source_seq FROM order_state WHERE NOT deleted;
CREATE OR REPLACE VIEW mart_daily AS SELECT CAST(ordered_at AS DATE) AS order_day,COUNT(*) AS paid_orders,SUM(amount_cents) AS paid_cents
 FROM live_orders WHERE status='paid' GROUP BY CAST(ordered_at AS DATE);
''')

def validate_snapshot(workspace,manifest):
    if set(manifest)!={'model_version','version_id','through_seq','rows','paid_cents','sha256','file'} or manifest['model_version']!=MODEL_VERSION:raise ValueError('Invalid publication manifest')
    path=(Path(workspace)/manifest['file']).resolve();versions=(Path(workspace)/'versions').resolve()
    if not path.is_relative_to(versions) or path.name!='orders.parquet' or not path.is_file():raise ValueError('Invalid artifact path')
    if file_digest(path)!=manifest['sha256']:raise ValueError('Artifact checksum mismatch')
    with connect() as connection:
        count,total=connection.execute("SELECT COUNT(*),COALESCE(SUM(amount_cents) FILTER (WHERE status='paid'),0) FROM read_parquet(?)",[str(path)]).fetchone()
    if count!=manifest['rows'] or total!=manifest['paid_cents']:raise ValueError('Artifact reconciliation failed')
    return manifest

def publish_pending(connection,workspace,fault=None):
    pending=connection.execute('SELECT batch_id,payload_hash,through_seq,version_id FROM publication_outbox WHERE NOT published ORDER BY through_seq,batch_id').fetchall()
    if len(pending)>1:raise RuntimeError('Recover pending publication before ingesting another batch')
    for batch_id,payload_hash,through_seq,version_id in pending:
        current=connection.execute('SELECT last_seq FROM cursor_state WHERE singleton=1').fetchone()[0]
        if through_seq!=current:raise RuntimeError('Publication checkpoint does not match current state')
        folder=workspace/'versions'/version_id;folder.mkdir(parents=True,exist_ok=True)
        manifest_path=folder/'manifest.json'
        if manifest_path.exists():
            manifest=json.loads(manifest_path.read_text(encoding='utf-8'));validate_snapshot(workspace,manifest)
            if manifest['version_id']!=version_id or manifest['through_seq']!=through_seq:raise ValueError('Manifest identity mismatch')
        else:
            parquet=folder/'orders.parquet';temporary=folder/(uuid.uuid4().hex+'.parquet.tmp')
            connection.execute("COPY (SELECT * FROM live_orders ORDER BY order_id) TO ? (FORMAT PARQUET, COMPRESSION ZSTD)",[str(temporary)])
            os.replace(temporary,parquet)
            count,total=connection.execute("SELECT COUNT(*),COALESCE(SUM(amount_cents) FILTER (WHERE status='paid'),0) FROM live_orders").fetchone()
            manifest={'model_version':MODEL_VERSION,'version_id':version_id,'through_seq':through_seq,'rows':count,'paid_cents':int(total),'sha256':file_digest(parquet),'file':parquet.relative_to(workspace).as_posix()}
            validate_snapshot(workspace,manifest);atomic_json(manifest_path,manifest)
        atomic_json(workspace/'current.json',manifest)
        if fault=='after_pointer':raise RuntimeError('Injected crash after pointer publication')
        connection.execute('UPDATE publication_outbox SET published=TRUE WHERE batch_id=?',[batch_id])
    return len(pending)

def process_batch(workspace,batch,fault=None):
    events=validate_batch(batch);payload_hash=digest(batch)
    workspace=Path(workspace).resolve()
    with writer_lock(workspace),connect(workspace/'warehouse.duckdb') as connection:
        initialize(connection)
        # Recovery happens before another batch can advance the current database state.
        publish_pending(connection,workspace)
        old=connection.execute('SELECT payload_hash FROM publication_outbox WHERE batch_id=?',[batch['batch_id']]).fetchone()
        if old:
            if old[0]!=payload_hash:raise ValueError('Batch id reused with different content')
            return {'replayed':True,'through_seq':connection.execute('SELECT last_seq FROM cursor_state').fetchone()[0]}
        checkpoint=connection.execute('SELECT last_seq FROM cursor_state WHERE singleton=1').fetchone()[0]
        if checkpoint!=batch['after_seq']:raise ValueError('Cursor mismatch; do not skip or rewind the committed range')
        connection.execute('BEGIN TRANSACTION')
        try:
            for event in events:
                connection.execute('INSERT INTO raw_events VALUES(?,?,?,?)',[event['event_id'],event['seq'],digest(event),canonical(event)])
                connection.execute('''INSERT INTO order_state VALUES(?,?,?,?,?,?,?)
 ON CONFLICT(order_id) DO UPDATE SET customer_id=excluded.customer_id,ordered_at=excluded.ordered_at,
 status=excluded.status,amount_cents=excluded.amount_cents,source_seq=excluded.source_seq,deleted=excluded.deleted
 WHERE excluded.source_seq>order_state.source_seq''',[event['order_id'],event['customer_id'],utc(event['ordered_at']),event['status'],event['amount_cents'],event['seq'],event['op']=='delete'])
            if fault=='before_commit':raise RuntimeError('Injected transaction failure')
            connection.execute('UPDATE cursor_state SET last_seq=? WHERE singleton=1',[batch['through_seq']])
            version_id=digest({'batch':payload_hash,'model':MODEL_VERSION})[:24]
            connection.execute('INSERT INTO publication_outbox VALUES(?,?,?,?,FALSE)',[batch['batch_id'],payload_hash,batch['through_seq'],version_id])
            connection.execute('COMMIT')
        except BaseException:
            connection.execute('ROLLBACK');raise
        if fault=='after_commit':raise RuntimeError('Injected crash after database commit')
        publish_pending(connection,workspace,fault)
        return {'replayed':False,'through_seq':batch['through_seq']}

def read_current(workspace):
    workspace=Path(workspace).resolve()
    return validate_snapshot(workspace,json.loads((workspace/'current.json').read_text(encoding='utf-8')))
