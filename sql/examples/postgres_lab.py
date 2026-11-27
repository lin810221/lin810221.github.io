"""Explicit, optional tests in a disposable PostgreSQL 19 database.

Set SQL_COURSE_PG_DSN only for a private course instance. The connected account
needs schema/role creation privileges; uniquely named objects are removed finally.
No existing application table is read or changed.
"""
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import json,os,uuid
import psycopg
from psycopg import sql

def run(dsn):
    schema='course_sql_'+uuid.uuid4().hex[:12];role='course_reader_'+uuid.uuid4().hex[:12]
    table=sql.Identifier(schema,'balances');tenant_table=sql.Identifier(schema,'tenants')
    report={}
    with psycopg.connect(dsn,autocommit=True) as admin:
        report['server_version']=admin.info.server_version
        if report['server_version']//10000!=19:raise RuntimeError('This lab targets PostgreSQL 19')
        admin.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(schema)))
        created_role=False
        try:
            admin.execute(sql.SQL('CREATE TABLE {} (id integer PRIMARY KEY, amount integer NOT NULL)').format(table))
            admin.execute(sql.SQL('INSERT INTO {} VALUES (1,100),(2,100)').format(table))
            for isolation,key in [('READ COMMITTED','read_committed'),('REPEATABLE READ','repeatable_read')]:
                admin.execute(sql.SQL('UPDATE {} SET amount=100 WHERE id=1').format(table))
                with psycopg.connect(dsn,autocommit=True) as reader:
                    reader.execute('BEGIN ISOLATION LEVEL '+isolation)
                    first=reader.execute(sql.SQL('SELECT amount FROM {} WHERE id=1').format(table)).fetchone()[0]
                    admin.execute(sql.SQL('UPDATE {} SET amount=200 WHERE id=1').format(table))
                    second=reader.execute(sql.SQL('SELECT amount FROM {} WHERE id=1').format(table)).fetchone()[0]
                    reader.execute('COMMIT');report[key]=[first,second]
            assert report['read_committed']==[100,200] and report['repeatable_read']==[100,100]
            with psycopg.connect(dsn,autocommit=True) as a,psycopg.connect(dsn,autocommit=True) as b:
                a.execute('BEGIN');a.execute(sql.SQL('SELECT * FROM {} WHERE id=1 FOR UPDATE').format(table))
                b.execute('BEGIN');skipped=b.execute(sql.SQL('SELECT id FROM {} ORDER BY id FOR UPDATE SKIP LOCKED').format(table)).fetchall()
                b.execute('ROLLBACK');a.execute('ROLLBACK')
                assert skipped==[(2,)];report['skip_locked']=[r[0] for r in skipped]
            admin.execute(sql.SQL('UPDATE {} SET amount=100').format(table))
            barrier=Barrier(2)
            def competing(key):
                with psycopg.connect(dsn,autocommit=True) as c:
                    try:
                        c.execute('BEGIN ISOLATION LEVEL SERIALIZABLE')
                        assert c.execute(sql.SQL('SELECT COUNT(*) FROM {} WHERE amount>0').format(table)).fetchone()[0]==2
                        barrier.wait(timeout=10)
                        c.execute(sql.SQL('UPDATE {} SET amount=0 WHERE id=%s').format(table),[key]);c.execute('COMMIT');return 'committed'
                    except psycopg.errors.SerializationFailure:
                        c.execute('ROLLBACK');return '40001'
            with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(competing,[1,2]))
            assert sorted(results)==['40001','committed'];report['serializable']=sorted(results)
            admin.execute(sql.SQL('CREATE ROLE {} NOLOGIN NOSUPERUSER NOBYPASSRLS').format(sql.Identifier(role)));created_role=True
            admin.execute(sql.SQL('CREATE TABLE {} (tenant_id integer,id integer PRIMARY KEY)').format(tenant_table))
            admin.execute(sql.SQL('INSERT INTO {} VALUES (1,10),(2,20)').format(tenant_table))
            admin.execute(sql.SQL('ALTER TABLE {} ENABLE ROW LEVEL SECURITY').format(tenant_table))
            admin.execute(sql.SQL('CREATE POLICY visible_tenant ON {} FOR SELECT TO {} USING (tenant_id=1)').format(tenant_table,sql.Identifier(role)))
            admin.execute(sql.SQL('GRANT USAGE ON SCHEMA {} TO {}').format(sql.Identifier(schema),sql.Identifier(role)))
            admin.execute(sql.SQL('GRANT SELECT ON {} TO {}').format(tenant_table,sql.Identifier(role)))
            with psycopg.connect(dsn,autocommit=True) as c:
                c.execute(sql.SQL('SET ROLE {}').format(sql.Identifier(role)))
                visible=c.execute(sql.SQL('SELECT tenant_id,id FROM {} ORDER BY id').format(tenant_table)).fetchall()
                assert visible==[(1,10)];report['rls_rows']=visible
            # PostgreSQL 19's get-or-create path returns the conflicting row.
            existing=admin.execute(sql.SQL('INSERT INTO {} VALUES (1,999) ON CONFLICT(id) DO SELECT RETURNING id,amount').format(table)).fetchone()
            assert existing[0]==1;report['on_conflict_do_select']=list(existing)
            ignored=admin.execute('''SELECT id,LAG(value) IGNORE NULLS OVER (ORDER BY id) AS previous
 FROM (VALUES(1,10),(2,NULL),(3,30)) AS readings(id,value) ORDER BY id''').fetchall()
            assert ignored==[(1,None),(2,10),(3,10)];report['ignore_nulls']=ignored
            report['parameters']=admin.execute('SELECT %s::text',["' OR 1=1 --"]).fetchone()[0]
            report['checks']='isolation/row-lock/SSI/RLS/PG19 features/parameter binding PASS'
            return report
        finally:
            admin.execute(sql.SQL('DROP SCHEMA {} CASCADE').format(sql.Identifier(schema)))
            if created_role:admin.execute(sql.SQL('DROP ROLE {}').format(sql.Identifier(role)))

if __name__=='__main__':
    dsn=os.environ.get('SQL_COURSE_PG_DSN')
    if not dsn:raise SystemExit('Set SQL_COURSE_PG_DSN for a private PostgreSQL 19 lab first')
    print(json.dumps(run(dsn),ensure_ascii=False,indent=2))
