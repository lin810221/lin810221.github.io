"""Run a deterministic lab with real DuckDB; no network or model service is used."""
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import argparse,json,shutil
from fixtures import ROOT,connect,seed,query_file
from contracts import cents,cursor_page,deduplicate,topological_sort,retry_delays,quality,scd_lookup,freshness
from pipeline import process_batch,read_current,writer_lock

LABS={
'01':'First SELECT and paid-order grain','02':'Order grain versus item grain','03':'Exact decimals, NULL and COUNT',
'04':'Primary, foreign and CHECK constraints','05':'Filtering and CASE','06':'GROUP BY and HAVING',
'07':'LEFT JOIN and preserved customers','08':'Pre-aggregation prevents fanout','09':'Recursive hierarchy with an explicit depth bound',
'10':'JSON extraction and rejected casts','11':'Deterministic ROWS and timestamp peers','12':'LAG and per-customer cumulative totals',
'13':'Atomic rollback','14':'MERGE updates an existing order','15':'Normalized customer dimension',
'16':'Half-open temporal dimension join','17':'Read a real execution plan','18':'Composite keyset pagination',
'19':'CSV explicit schema and quoted cells','20':'Parquet round-trip and projection','21':'Typed staging and quarantine labels',
'22':'Deterministic deduplication','23':'Timestamp and id cursor pages','24':'Ordered event replay and source bounds',
'25':'DAG dependency sorting and cycle rejection','26':'Bounded retries without sleeping','27':'Completeness and empty denominators',
'28':'Order-to-item reconciliation','29':'Regional paid-order mart','30':'Detect overlapping SCD histories',
'31':'Bound parameters reject SQL injection semantics','32':'Closed-database backup and restore','33':'First DataHarbor publication',
'34':'Incremental correction and delete','35':'Crash after commit and recovery','36':'Acceptance: retry, checksums and latest publication'}

@contextmanager
def scratch():
    # Normal pathlib permissions also work with newer Windows Python runtimes.
    import uuid
    root=ROOT/'.runtime';root.mkdir(exist_ok=True)
    path=root/uuid.uuid4().hex;path.mkdir()
    try:yield path
    finally:shutil.rmtree(path)

def load_batch(n):return json.loads((ROOT/'data'/f'batch-{n:03d}.json').read_text(encoding='utf-8'))

def run_lab(name):
    if name not in LABS:raise ValueError('Unknown lab')
    with scratch() as work,connect() as connection:
        seed(connection)
        path=ROOT/'queries'/f'{name}.sql'
        if path.is_file():
            if name=='31':return connection.execute(path.read_text(encoding='utf-8'),["' OR 1=1 --"]).fetchall()
            return query_file(connection,name)
        if name=='04':
            results=[]
            for statement in ["INSERT INTO orders VALUES (101,1,now(),'paid',1)","INSERT INTO orders VALUES (999,99,now(),'paid',1)","INSERT INTO orders VALUES (999,1,now(),'paid',-1)"]:
                try:connection.execute(statement)
                except Exception as exc:results.append(type(exc).__name__)
            return {'rejected':results,'orders':connection.execute('SELECT COUNT(*) FROM orders').fetchone()[0]}
        if name=='13':
            connection.execute('BEGIN');connection.execute('UPDATE orders SET amount_cents=1 WHERE order_id=101');connection.execute('ROLLBACK')
            return connection.execute('SELECT amount_cents FROM orders WHERE order_id=101').fetchone()
        if name=='19':
            return connection.execute("SELECT external_id,amount,comment FROM read_csv(?,header=true,columns={'external_id':'VARCHAR','amount':'DECIMAL(12,2)','comment':'VARCHAR'}) ORDER BY external_id",[str(ROOT/'data/orders_import.csv')]).fetchall()
        if name=='20':
            target=work/'orders.parquet';connection.execute("COPY (SELECT * FROM orders ORDER BY order_id) TO ? (FORMAT PARQUET, COMPRESSION ZSTD)",[str(target)])
            return connection.execute("SELECT COUNT(*),SUM(amount_cents) FROM read_parquet(?)",[str(target)]).fetchone()
        if name=='23':
            rows=[{'id':i,'updated_at':'2026-11-01T00:00:00Z'} for i in [3,1,2]]
            return [r['id'] for r in cursor_page(rows,('2026-11-01T00:00:00Z',1),2)]
        if name=='24':
            from pipeline import validate_batch
            return {'events':len(validate_batch(load_batch(1))),'same_event_twice':deduplicate([{'id':1,'seq':1},{'id':1,'seq':1}])}
        if name=='25':return topological_sort({'extract':[],'stage':['extract'],'validate':['stage'],'publish':['validate']})
        if name=='26':return retry_delays(5,1,4)
        if name=='32':
            source=work/'source.duckdb'
            with connect(source) as c:seed(c)
            # Source is closed, and this workspace is exclusively owned by this lab.
            shutil.copy2(source,work/'restored.duckdb')
            with connect(work/'restored.duckdb') as c:return c.execute('SELECT COUNT(*),SUM(amount_cents) FROM orders').fetchone()
        if name in ('33','34','35','36'):
            project=work/'harbor';first=load_batch(1)
            if name=='35':
                try:process_batch(project,first,'after_commit')
                except RuntimeError:pass
            process_batch(project,first)
            if name in ('34','36'):process_batch(project,load_batch(2))
            if name=='36':process_batch(project,first);process_batch(project,load_batch(2))
            manifest=read_current(project)
            return {k:manifest[k] for k in ('through_seq','rows','paid_cents')}
    raise ValueError('Lab has no implementation')

def main(name=None):
    if name is None:
        parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('lab',nargs='?');parser.add_argument('--list',action='store_true');args=parser.parse_args()
        if args.list:
            for key,title in LABS.items():print(key,title)
            return
        if not args.lab:parser.error('Choose a lab or --list')
        name=args.lab.zfill(2)
    print(json.dumps({'lab':name,'goal':LABS[name],'result':run_lab(name)},ensure_ascii=False,default=str,indent=2))

if __name__=='__main__':main()
