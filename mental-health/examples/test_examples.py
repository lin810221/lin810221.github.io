"""Numerical, missingness and scope contracts for original educational examples."""
from copy import deepcopy
from pathlib import Path
import csv,json,math,tempfile,unittest
from psych_core import *
from psych_data import DATA,diary,diary_arithmetic,workdays
from reporting import deliver,diary_svg

class ObservationTests(unittest.TestCase):
    def test_available(self):self.assertEqual(diary_summary([4,None,6])['available_mean'],5)
    def test_complete_unknown(self):self.assertIsNone(diary_summary([4,None,6])['complete_mean'])
    def test_median(self):self.assertEqual(diary_summary([0,5,10])['median'],5)
    def test_zero_observed(self):self.assertEqual(diary_summary([0])['observed'],1)
    def test_empty(self):self.assertIsNone(diary_summary([])['available_mean'])
    def test_all_missing(self):self.assertIsNone(diary_summary([None,None])['median'])
    def test_scale_range(self):
        for value in [-1,11,True,float('nan'),float('inf')]:
            with self.assertRaises(ValueError):diary_summary([value])
    def test_no_risk_band(self):self.assertNotIn('diagnosis',diary_summary([10]))
    def test_rolling(self):self.assertEqual(rolling([1,2,3,4]),[None,None,2,3])
    def test_rolling_gap(self):self.assertEqual(rolling([1,None,3,4]),[None,None,None,None])
    def test_window_domain(self):
        for n in [0,True,1.5,-1]:
            with self.assertRaises(ValueError):rolling([1,2],n)
    def test_action_false_known(self):self.assertEqual(opportunity([True,False,None])['observed'],2)
    def test_action_available(self):self.assertEqual(opportunity([True,False,None])['available_fraction'],.5)
    def test_action_complete_unknown(self):self.assertIsNone(opportunity([True,None])['complete_fraction'])
    def test_action_empty(self):self.assertIsNone(opportunity([])['available_fraction'])
    def test_action_strict_type(self):
        with self.assertRaises(ValueError):opportunity([1])
    def test_subtotal(self):self.assertEqual(minutes_total([10,None,0])['known_subtotal'],10)
    def test_total_unknown(self):self.assertIsNone(minutes_total([10,None])['complete_total'])
    def test_empty_additive_identity(self):self.assertEqual(minutes_total([])['complete_total'],0)

class TimingTests(unittest.TestCase):
    def test_switches(self):self.assertEqual(task_switch()['switches'],5)
    def test_switch_units(self):self.assertEqual(task_switch()['total_seconds'],7350)
    def test_single_block(self):self.assertEqual(task_switch(1)['assumed_overhead_seconds'],0)
    def test_switch_domain(self):
        for n in [0,True,2.5]:
            with self.assertRaises(ValueError):task_switch(n)
    def test_midnight(self):self.assertEqual(time_window()['minutes'],480)
    def test_same_day(self):self.assertEqual(time_window('09:00','10:30',False)['minutes'],90)
    def test_day_flag(self):
        with self.assertRaises(ValueError):time_window('23:00','07:00',False)
    def test_bad_clock(self):
        for clock in ['24:00','7:00','07:60',None]:
            with self.assertRaises(ValueError):clock_minute(clock)
    def test_full_day(self):self.assertEqual(time_window('07:00','07:00',True)['minutes'],1440)
    def test_no_sleep_prescription(self):self.assertIn('not actual sleep',time_window()['scope'])
    def test_breath_total(self):self.assertEqual(breath_cycle()['total_seconds'],30)
    def test_breath_rate(self):self.assertEqual(breath_cycle()['cycles_per_minute'],6)
    def test_breath_domain(self):
        for args in [(0,6,3),(4,6,0),(4,6,1.5)]:
            with self.assertRaises(ValueError):breath_cycle(*args)
    def test_known_plan(self):self.assertEqual(work_ledger(240,[90,60,30],30)['difference_minutes'],30)
    def test_missing_plan(self):self.assertIsNone(work_ledger()['difference_minutes'])
    def test_short_plan(self):self.assertEqual(work_ledger(180,[90,120],30)['difference_minutes'],-60)

class ModelTests(unittest.TestCase):
    def test_toy_zero(self):self.assertEqual(recovery_analogy(0)['rows'][-1]['state'],0)
    def test_toy_no_decay(self):self.assertEqual(recovery_analogy(10,1)['rows'][-1]['state'],30)
    def test_toy_full_decay(self):self.assertEqual(recovery_analogy(10,0)['rows'][-1]['state'],0)
    def test_toy_scope(self):self.assertIn('not human stress',recovery_analogy()['scope'])
    def test_toy_domain(self):
        for args in [(10,1.1),(10,.7,0),(True,.7,28)]:
            with self.assertRaises(ValueError):recovery_analogy(*args)
    def test_association(self):self.assertAlmostEqual(paired_association([1,2,3],[3,2,1])['r'],-1)
    def test_association_pairwise(self):self.assertEqual(paired_association([1,None,3],[1,2,3])['paired_n'],2)
    def test_constant_unknown(self):self.assertIsNone(paired_association([1,1],[1,2])['r'])
    def test_insufficient_unknown(self):self.assertIsNone(paired_association([None,1],[2,2])['r'])
    def test_pairs_length(self):
        with self.assertRaises(ValueError):paired_association([1],[1,2])
    def test_bayes_counts(self):self.assertEqual(screening()['tp'],400)
    def test_bayes_ppv(self):self.assertAlmostEqual(screening()['ppv'],400/1350)
    def test_bayes_total(self):self.assertAlmostEqual(sum(screening()[k] for k in ['tp','fp','tn','fn']),10000)
    def test_bayes_base_rate(self):self.assertGreater(screening(prevalence=.2)['ppv'],screening()['ppv'])
    def test_bayes_no_positives(self):self.assertIsNone(screening(prevalence=0,specificity=1)['ppv'])
    def test_bayes_domain(self):
        for args in [(0,), (100,.1,1.1), (10.5,)]:
            with self.assertRaises(ValueError):screening(*args)
    def test_standardized_equal_sd(self):self.assertAlmostEqual(standardized_difference(50,45,10,10)['cohen_d'],-.5)
    def test_standardized_direction(self):self.assertGreater(standardized_difference(45,50)['cohen_d'],0)
    def test_hedges_correction(self):
        result=standardized_difference();self.assertLess(abs(result['hedges_g_approx']),abs(result['cohen_d']))
    def test_no_raw_difference(self):self.assertEqual(standardized_difference(50,50)['cohen_d'],0)
    def test_standardized_domain(self):
        for args in [(50,45,0,10),(50,45,10,10,1,30)]:
            with self.assertRaises(ValueError):standardized_difference(*args)

class ContextTests(unittest.TestCase):
    def test_false_is_known(self):self.assertEqual(coverage({'share':False},['share'])['known'],['share'])
    def test_missing_context(self):self.assertEqual(coverage({'a':None},['a','b'])['unknown'],['a','b'])
    def test_case_is_copy(self):
        a=thought_case();a['observation']='changed';self.assertNotEqual(thought_case()['observation'],'changed')
    def test_case_unknown(self):
        with self.assertRaises(ValueError):thought_case('unknown')
    def test_support_general(self):self.assertIn('not automated crisis',support_response('urgent')['scope'])
    def test_no_safety_score(self):self.assertNotIn('score',support_response('urgent'))
    def test_support_unknown(self):
        with self.assertRaises(ValueError):support_response('other')

class DataTests(unittest.TestCase):
    def changed_diary(self,change):
        with (DATA/'diary.csv').open(encoding='utf-8',newline='') as stream:rows=list(csv.DictReader(stream))
        change(rows)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'altered.csv'
            with p.open('w',encoding='utf-8',newline='') as stream:
                writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
            with self.assertRaises(ValueError):diary(p)
    def test_duplicate_date(self):self.changed_diary(lambda rows:rows[1].update(date=rows[0]['date']))
    def test_status_conflict(self):self.changed_diary(lambda rows:rows[0].update(status='missing'))
    def test_real_data_rejected(self):self.changed_diary(lambda rows:rows[0].update(synthetic='false'))
    def test_other_scale_rejected(self):self.changed_diary(lambda rows:rows[0].update(scale='clinical_scale'))
    def test_incomplete_schedule_rejected(self):self.changed_diary(lambda rows:rows.pop())
    def test_slots(self):self.assertEqual(len(diary()),14)
    def test_two_missing(self):self.assertEqual(diary_arithmetic()['summary']['missing'],2)
    def test_complete_unknown(self):self.assertIsNone(diary_arithmetic()['summary']['complete_mean'])
    def test_workdays(self):self.assertEqual(len(workdays()),3)
    def test_original_scale_only(self):
        self.assertTrue(all(row['scale']=='original_diary_0_10' for row in diary()))
    def test_source_states(self):
        sources=json.loads((DATA/'sources.json').read_text(encoding='utf-8'));self.assertTrue(any('in development' in s['status'] for s in sources))
    def test_svg_unknown_visible(self):self.assertIn('? = missing',diary_svg(diary()))
    def test_svg_no_nan(self):self.assertNotIn('NaN',diary_svg(diary()))
    def test_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)/'new';report=deliver(base);self.assertTrue(all(report['checks'].values()));self.assertEqual(len(report['data_sha256']),5)
            self.assertEqual({p.name for p in base.iterdir()},{'diary_observations.csv','diary_observations.svg','report.json'})
            self.assertIsNone(json.loads((base/'report.json').read_text(encoding='utf-8'))['observations']['summary']['complete_mean'])
    def test_existing_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileExistsError):deliver(Path(tmp))

if __name__=='__main__':unittest.main()
