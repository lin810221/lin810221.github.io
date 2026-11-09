"""Behavioral/numeric contracts for offline educational records and reports."""
import csv,json,math,tempfile,unittest
from pathlib import Path
from training_core import *
from training_data import DATA,sessions,weeks,lifts,lift_totals
from reporting import deliver,svg_load

class MechanicsTests(unittest.TestCase):
    def test_torque_perpendicular(self):self.assertAlmostEqual(torque(100,.3,90),30)
    def test_torque_angle(self):self.assertAlmostEqual(torque(100,.3,30),15)
    def test_torque_parallel(self):self.assertAlmostEqual(torque(100,.3,180),0)
    def test_torque_domain(self):
        for args in [(-1,.3,90),(100,-1,90),(100,.3,181)]:
            with self.assertRaises(ValueError):torque(*args)
    def test_work_and_power(self):
        self.assertAlmostEqual(external_work(20,.5,2)['joules'],98.0665);self.assertAlmostEqual(external_work(20,.5,2)['watts'],49.03325)
    def test_zero_displacement(self):self.assertEqual(external_work(20,0,2)['joules'],0)
    def test_power_zero_time(self):
        with self.assertRaises(ValueError):external_work(20,.5,0)
    def test_impulse(self):self.assertEqual(impulse(200,.2),40)
    def test_oxygen(self):self.assertAlmostEqual(oxygen_units(2500,70),35.714285714)
    def test_cardiac_output(self):self.assertEqual(cardiac_output(120,100),12)
    def test_nonfinite_bool(self):
        for value in [True,False,float('nan'),float('inf'),-1]:
            with self.assertRaises(ValueError):nonnegative(value=value)

class ResistanceTests(unittest.TestCase):
    def test_relative_load(self):self.assertEqual(relative_load(60,80),75)
    def test_above_reference_preserved(self):self.assertEqual(relative_load(90,80),112.5)
    def test_zero_reference(self):
        with self.assertRaises(ValueError):relative_load(60,0)
    def test_epley(self):self.assertEqual(estimated_1rm(60,5),70)
    def test_brzycki(self):self.assertEqual(estimated_1rm(60,5,'brzycki'),67.5)
    def test_single_actual_rep(self):self.assertEqual(estimated_1rm(60,1),60)
    def test_estimate_domain(self):
        for reps in [0,11,True,2.5]:
            with self.assertRaises(ValueError):estimated_1rm(60,reps)
        with self.assertRaises(ValueError):estimated_1rm(60,5,'unknown')
    def test_rir_scale(self):self.assertEqual(rir_rpe(2)['rpe'],8)
    def test_rir_not_borg(self):
        with self.assertRaises(ValueError):rir_rpe(2,'Borg_6_20')
    def test_rir_domain(self):
        for value in [-1,5,11,float('nan')]:
            with self.assertRaises(ValueError):rir_rpe(value)
    def test_volume(self):self.assertEqual(volume([{'reps':8,'load_kg':40}]*3)['volume_load_kg_reps'],960)
    def test_unknown_volume(self):
        r=volume([{'reps':8,'load_kg':40},{'reps':8,'load_kg':None}]);self.assertIsNone(r['volume_load_kg_reps']);self.assertEqual(r['known_volume_load'],320)
    def test_zero_reps_unknown(self):self.assertEqual(volume([{'reps':0,'load_kg':None}])['volume_load_kg_reps'],0)
    def test_invalid_set(self):
        with self.assertRaises(ValueError):volume([{'reps':1.5,'load_kg':40}])
    def test_direct_sets(self):self.assertEqual(direct_sets([{'primary_target':'A','sets':3},{'primary_target':'A','sets':2}]),{'A':5})
    def test_progression_missing(self):
        r=progression_state([10,10],[2,None]);self.assertTrue(r['all_reach_upper']);self.assertFalse(r['rir_complete'])
    def test_progression_alignment(self):
        with self.assertRaises(ValueError):progression_state([10],[2,2])

class AerobicTests(unittest.TestCase):
    def test_pace(self):
        r=pace(5,30);self.assertEqual(r['seconds_per_km'],360);self.assertEqual(r['km_h'],10)
    def test_pace_roundtrip(self):
        for d,t in [(1,5),(5,31),(10,52)]:self.assertAlmostEqual(pace(d,t)['km_h']*pace(d,t)['seconds_per_km'],3600)
    def test_zero_distance_time(self):
        for args in [(0,30),(5,0)]:
            with self.assertRaises(ValueError):pace(*args)
    def test_interval_no_final_rest(self):
        r=intervals();self.assertEqual(r['work_s'],360);self.assertEqual(r['recovery_s'],450);self.assertEqual(r['total_s'],1710)
    def test_interval_final_rest(self):self.assertEqual(intervals(final_recovery=True)['total_s'],1800)
    def test_single_interval(self):self.assertEqual(intervals(1,60,90,0,0)['total_s'],60)
    def test_interval_bad_count(self):
        for value in [0,1.5,True]:
            with self.assertRaises(ValueError):intervals(value)
    def test_hrr(self):self.assertEqual(heart_reserve(60,180,.6)['bpm'],132)
    def test_hrr_endpoints(self):
        self.assertEqual(heart_reserve(60,180,0)['bpm'],60);self.assertEqual(heart_reserve(60,180,1)['bpm'],180)
    def test_hrr_invalid(self):
        for args in [(60,50,.6),(60,180,1.1)]:
            with self.assertRaises(ValueError):heart_reserve(*args)
    def test_met_gross_net(self):
        r=standard_met(5,60,30);self.assertEqual(r['gross_kcal'],157.5);self.assertEqual(r['above_standard_rest_kcal'],126)
    def test_met_rest(self):self.assertEqual(standard_met(1,60,30)['above_standard_rest_kcal'],0)
    def test_guideline_equivalence(self):self.assertEqual(activity_equivalent(90,30)['moderate_equivalent_minutes'],150)
    def test_population_not_silently_changed(self):
        with self.assertRaises(ValueError):activity_equivalent(60,0,'child')

class LoadMeasurementTests(unittest.TestCase):
    def test_session_load(self):self.assertEqual(session_load(45,5),225)
    def test_session_scale_is_distinct(self):
        with self.assertRaises(ValueError):session_load(45,8,'resistance_RIR_10')
    def test_week_rest(self):self.assertEqual(weekly_load([200,0,200,0,200,0,0])['total'],600)
    def test_week_unknown(self):
        r=weekly_load([200,0,None,0,200,0,0]);self.assertIsNone(r['total']);self.assertEqual(r['known_subtotal'],400)
    def test_seven_day_scope(self):
        with self.assertRaises(ValueError):weekly_load([200]*6)
    def test_uncoupled_ratio(self):self.assertEqual(load_ratio(1100,[900,1000,1100,1000])['ratio'],1.1)
    def test_ratio_zero_missing(self):
        self.assertIsNone(load_ratio(100,[0]*4)['ratio']);self.assertIsNone(load_ratio(100,[1,2,None,4])['ratio'])
    def test_ratio_scope_not_safety(self):self.assertIn('no safe zone',load_ratio(1100,[1000]*4)['scope'])
    def test_rolling_requires_full_window(self):self.assertEqual(rolling([1,2,3],3),[None,None,2])
    def test_rolling_missing_not_zero(self):self.assertEqual(rolling([1,None,3,4],2),[None,None,None,3.5])
    def test_measurement_bias(self):
        r=measurement([10,20,30],[11,21,31]);self.assertEqual(r['bias'],1);self.assertEqual(r['mdc95'],0)
    def test_mdc(self):
        r=measurement([10,20,30],[9,20,31]);self.assertEqual(r['sd_difference'],1);self.assertAlmostEqual(r['mdc95'],1.96)
    def test_measurement_alignment(self):
        with self.assertRaises(ValueError):measurement([1],[1,2])
    def test_zero_baseline_change(self):self.assertIsNone(change(0,1)['percent_change'])
    def test_direction_recorded(self):self.assertEqual(change(30,28,True)['direction'],'lower_is_better')
    def test_toy_response_zero(self):self.assertEqual(fitness_fatigue([0,0])['rows'][-1]['toy_response'],0)
    def test_toy_decay(self):
        r=fitness_fatigue([100,0])['rows'];self.assertLess(r[1]['fatigue_component'],r[0]['fatigue_component'])
    def test_toy_scope(self):self.assertIn('not readiness',fitness_fatigue([100])['scope'])

class DataDeliveryTests(unittest.TestCase):
    def test_records_explicit(self):self.assertEqual(len(sessions()),28)
    def test_complete_and_incomplete_weeks(self):
        r=weeks();self.assertEqual(len(r),4);self.assertIsNotNone(r['week1']['session_load']['total']);self.assertIsNone(r['week4']['session_load']['total'])
    def test_external_bodyweight_not_invented(self):self.assertIsNone(lift_totals()['pushup']['volume_load_kg_reps'])
    def test_lifts_count(self):self.assertEqual(len(lifts()),9)
    def test_schema_rejects_duplicate_days(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'bad.csv';text=(DATA/'sessions.csv').read_text(encoding='utf-8').splitlines();p.write_text('\n'.join([*text,text[1]])+'\n',encoding='utf-8')
            with self.assertRaises(ValueError):sessions(p)
    def test_observed_intensity_minutes_cannot_double_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            with (DATA/'sessions.csv').open(encoding='utf-8',newline='') as stream:
                rows=list(csv.DictReader(stream))
            keys=list(rows[0]);rows[0]['moderate_minutes']='50';rows[0]['vigorous_minutes']='30'
            p=Path(tmp)/'bad.csv'
            with p.open('w',encoding='utf-8',newline='') as stream:
                writer=csv.DictWriter(stream,fieldnames=keys);writer.writeheader();writer.writerows(rows)
            with self.assertRaises(ValueError):sessions(p)
    def test_svg_unknown_explicit(self):self.assertIn('unknown total',svg_load(weeks()))
    def test_full_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'report';result=deliver(dest);self.assertTrue(all(result['checks'].values()))
            r=json.loads((dest/'report.json').read_text(encoding='utf-8'));self.assertEqual(len(r['data_sha256']),5);self.assertTrue(r['synthetic'])
            with (dest/'weekly_load.csv').open(encoding='utf-8') as stream:rows=list(csv.DictReader(stream))
            self.assertEqual(rows[3]['total_au'],'');self.assertNotEqual(rows[3]['known_subtotal_au'],'')
            self.assertIn('not rest',(dest/'training_load.svg').read_text(encoding='utf-8'))
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileExistsError):deliver(Path(tmp))

if __name__=='__main__':unittest.main()
