"""Boundary tests against real DuckDB, files and the complete DataHarbor pipeline."""
from copy import deepcopy
from pathlib import Path
import json,unittest
import duckdb
from fixtures import connect,seed,query_file,ROOT
from contracts import cents,utc,cursor_page,deduplicate,topological_sort,retry_delays,quality,validate_scd,scd_lookup,freshness
from pipeline import process_batch,read_current,validate_batch,writer_lock
from run_lab import run_lab,scratch,load_batch,LABS
from orchestrator import run_dag,TransientError,TaskFailed
from warehouse import build_star

class SQLTests(unittest.TestCase):
    def test_current_engine(self):self.assertEqual(duckdb.__version__,'2.0.1')
    def test_grain(self):self.assertEqual(run_lab('02'),[('orders',5,5),('items',6,5)])
    def test_null_and_decimal(self):
        row=run_lab('03')[0];self.assertEqual(row[:2],(4,2));self.assertEqual(str(row[2]),'12.50');self.assertIsNone(row[3]);self.assertTrue(row[4])
    def test_constraints(self):
        report=run_lab('04');self.assertEqual(report['orders'],5);self.assertEqual(len(report['rejected']),3)
    def test_paid_group(self):self.assertEqual(run_lab('06'),[(1,2,8000),(2,1,4000)])
    def test_left_join(self):self.assertEqual(run_lab('07'),[(1,2),(2,1),(3,1),(4,0)])
    def test_fanout_repaired(self):self.assertEqual(run_lab('08'),[(101,3000,500,2500),(102,5000,1500,3500),(104,4000,0,4000),(105,1000,0,1000)])
    def test_recursive_tree(self):self.assertEqual([r[0] for r in run_lab('09')],[1,2,5,3,4])
    def test_json_reject(self):self.assertEqual(run_lab('10'),[('101',None)])
    def test_window_frames(self):
        rows=run_lab('11');self.assertEqual([r[2] for r in rows],[3000,8000,10000,14000,15000]);self.assertEqual([r[3] for r in rows],[3000,10000,10000,15000,15000])
    def test_rollback(self):self.assertEqual(run_lab('13'),(3000,))
    def test_merge(self):self.assertEqual(run_lab('14'),[(102,4500),(105,1200)])
    def test_temporal_join(self):self.assertEqual(run_lab('16'),[(101,'north'),(102,'south')])
    def test_explain(self):self.assertIn('GROUP',str(run_lab('17')).upper())
    def test_keyset(self):self.assertEqual([r[0] for r in run_lab('18')],[103,104])
    def test_csv_quoted_and_leading_zero(self):
        rows=run_lab('19');self.assertEqual(rows[0][0],'001');self.assertEqual(rows[0][2],'quoted, comma');self.assertEqual(rows[2][2],'text with "quotes"')
    def test_parquet(self):self.assertEqual(run_lab('20'),(5,15000))
    def test_staging_reasons(self):self.assertEqual([r[3] for r in run_lab('21')],['valid','invalid','missing'])
    def test_rank_dedup(self):self.assertEqual(run_lab('22'),[(1,11,'new'),(2,9,'other')])
    def test_reconciliation(self):self.assertEqual(run_lab('28'),[])
    def test_mart(self):self.assertEqual(run_lab('29'),[('north',3,9000),('south',1,4000)])
    def test_bound_sql_injection(self):self.assertEqual(run_lab('31'),[])
    def test_backup_restore(self):self.assertEqual(run_lab('32'),(5,15000))
    def test_every_real_entry_runs(self):
        for name in LABS:
            with self.subTest(lab=name):self.assertIsNotNone(run_lab(name))

class ContractTests(unittest.TestCase):
    def test_exact_money(self):self.assertEqual(cents('12.50'),1250)
    def test_reject_bad_money(self):
        for value in ['1.001','-1','NaN','Infinity']:
            with self.subTest(value=value),self.assertRaises(ValueError):cents(value)
    def test_utc_requires_offset(self):
        with self.assertRaises(ValueError):utc('2026-11-01T12:00:00')
        self.assertEqual(utc('2026-11-01T08:00:00+08:00'),utc('2026-11-01T00:00:00Z'))
    def test_cursor_ties(self):self.assertEqual(run_lab('23'),[2,3])
    def test_ambiguous_dedup(self):
        with self.assertRaises(ValueError):deduplicate([dict(id=1,seq=2,x='a'),dict(id=1,seq=2,x='b')])
    def test_dag_cycle(self):
        with self.assertRaises(ValueError):topological_sort({'a':['b'],'b':['a']})
        with self.assertRaises(ValueError):topological_sort({'a':['missing']})
    def test_retry_budget(self):self.assertEqual(retry_delays(5,1,4),[1,2,4,4])
    def test_quality_empty(self):self.assertIsNone(quality([])['completeness'])
    def test_quality_denominator(self):
        r=quality([dict(id=1,amount_cents=1),dict(id=1,amount_cents=None)]);self.assertEqual(r['completeness'],.5);self.assertEqual(r['duplicate_excess'],1);self.assertEqual(r['uniqueness'],.5)
        self.assertIsNone(quality([dict(id=None,amount_cents=1)])['uniqueness'])
    def test_scd_boundary(self):
        rows=[dict(id=1,valid_from='2026-01-01T00:00:00Z',valid_to='2026-11-01T00:00:00Z',region='north'),dict(id=1,valid_from='2026-11-01T00:00:00Z',valid_to=None,region='south')]
        self.assertEqual(scd_lookup(rows,1,'2026-11-01T00:00:00Z')['region'],'south')
        rows[0]['valid_to']='2026-11-02T00:00:00Z'
        with self.assertRaises(ValueError):validate_scd(rows)
    def test_freshness_clock(self):
        self.assertEqual(freshness('2026-11-01T01:00:00Z','2026-11-01T00:00:00Z'),3600)
        with self.assertRaises(ValueError):freshness('2026-11-01T00:00:00Z','2026-11-01T01:00:00Z')

class PipelineTests(unittest.TestCase):
    def test_complete_incremental_and_old_retry(self):
        with scratch() as w:
            process_batch(w,load_batch(1));process_batch(w,load_batch(2));old=read_current(w)
            self.assertEqual((old['through_seq'],old['rows'],old['paid_cents']),(8,4,11500))
            self.assertTrue(process_batch(w,load_batch(1))['replayed']);self.assertEqual(read_current(w),old)
            with connect(w/'warehouse.duckdb') as c:
                self.assertEqual(c.execute('SELECT COUNT(*) FROM raw_events').fetchone()[0],8)
                self.assertTrue(c.execute('SELECT deleted FROM order_state WHERE order_id=101').fetchone()[0])
    def test_failure_before_commit(self):
        with scratch() as w:
            with self.assertRaises(RuntimeError):process_batch(w,load_batch(1),'before_commit')
            with connect(w/'warehouse.duckdb') as c:
                self.assertEqual(c.execute('SELECT last_seq FROM cursor_state').fetchone()[0],0);self.assertEqual(c.execute('SELECT COUNT(*) FROM order_state').fetchone()[0],0)
            self.assertFalse((w/'current.json').exists());process_batch(w,load_batch(1));self.assertEqual(read_current(w)['through_seq'],4)
    def test_recovery_after_commit(self):
        with scratch() as w:
            with self.assertRaises(RuntimeError):process_batch(w,load_batch(1),'after_commit')
            self.assertFalse((w/'current.json').exists());process_batch(w,load_batch(2));self.assertEqual(read_current(w)['through_seq'],8)
    def test_recovery_after_pointer(self):
        with scratch() as w:
            with self.assertRaises(RuntimeError):process_batch(w,load_batch(1),'after_pointer')
            old=read_current(w);process_batch(w,load_batch(1));self.assertEqual(read_current(w),old)
    def test_batch_id_conflict(self):
        with scratch() as w:
            first=load_batch(1);process_batch(w,first);first['events'][0]['amount_cents']=999
            with self.assertRaises(ValueError):process_batch(w,first)
            self.assertEqual(read_current(w)['paid_cents'],12000)
    def test_duplicate_event_exact(self):
        batch=load_batch(1);batch['events'].append(deepcopy(batch['events'][0]));self.assertEqual(len(validate_batch(batch)),4)
    def test_missing_sequence(self):
        batch=load_batch(1);batch['events'].pop()
        with self.assertRaises(ValueError):validate_batch(batch)
    def test_conflicting_event(self):
        batch=load_batch(1);bad=deepcopy(batch['events'][0]);bad['amount_cents']=999;batch['events'].append(bad)
        with self.assertRaises(ValueError):validate_batch(batch)
    def test_reject_bad_input_before_storage(self):
        for field,value in [('amount_cents',True),('amount_cents',-1),('ordered_at','2026-01-01T00:00:00'),('status','unknown')]:
            with scratch() as w:
                batch=load_batch(1);batch['events'][0][field]=value
                with self.subTest(field=field,value=value),self.assertRaises(ValueError):process_batch(w/'not-created',batch)
                self.assertFalse((w/'not-created').exists())
    def test_cursor_gap(self):
        with scratch() as w:
            with self.assertRaises(ValueError):process_batch(w,load_batch(2))
            with connect(w/'warehouse.duckdb') as c:self.assertEqual(c.execute('SELECT last_seq FROM cursor_state').fetchone()[0],0)
    def test_corrupted_artifact(self):
        with scratch() as w:
            process_batch(w,load_batch(1));manifest=read_current(w);(w/manifest['file']).write_bytes(b'broken')
            with self.assertRaises(ValueError):read_current(w)
    def test_writer_lock(self):
        with scratch() as w,writer_lock(w):
            with self.assertRaises(RuntimeError),writer_lock(w):pass
    def test_manifest_path_escape(self):
        from pipeline import validate_snapshot
        with scratch() as w:
            process_batch(w,load_batch(1));manifest=read_current(w);manifest['file']='../orders.parquet'
            with self.assertRaises(ValueError):validate_snapshot(w,manifest)

class EngineeringTests(unittest.TestCase):
    def test_real_dag_retry_and_dependency(self):
        calls=[];waits=[]
        def first():
            calls.append('first')
            if len(calls)<3:raise TransientError('retry')
            return 7
        report=run_dag({'first':[],'second':['first']},{'first':first,'second':lambda:11},sleeper=waits.append)
        self.assertEqual(waits,[1,2]);self.assertEqual(report['results'],{'first':7,'second':11})
    def test_permanent_failure_blocks_downstream(self):
        calls=[]
        def bad():raise ValueError('contract')
        with self.assertRaises(TaskFailed) as error:run_dag({'a':[],'b':['a']},{'a':bad,'b':lambda:calls.append('b')},sleeper=lambda _:None)
        self.assertEqual(calls,[]);self.assertEqual(len(error.exception.events),1)
    def test_star_schema_historical_region(self):
        with connect() as c:
            seed(c);self.assertEqual(build_star(c),[('north',2,4000),('south',2,9000)])
            self.assertEqual(c.execute('SELECT COUNT(*) FROM analytics.fact_order').fetchone()[0],5)
    def test_complete_workflow_replay(self):
        from workflow import workflow
        with scratch() as w:
            first=workflow(w);second=workflow(w)
            self.assertEqual(first['results']['verify_snapshot'],second['results']['verify_snapshot'])
            self.assertTrue(second['results']['load_first']['replayed'])

if __name__=='__main__':unittest.main()
