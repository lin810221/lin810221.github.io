"""Arithmetic and scope contracts; no personal safety or diagnosis assertions."""
from pathlib import Path
import csv,json,math,tempfile,unittest
from ergo_core import *
from ergo_data import DATA,observations,observation_summary,workers,lift_cases
from reporting import deliver,observation_svg

class MechanicalTests(unittest.TestCase):
    def test_mass_force(self):self.assertAlmostEqual(mass_force(10),98.0665)
    def test_moment(self):self.assertAlmostEqual(moment(100,.3,90),30)
    def test_half_moment(self):self.assertAlmostEqual(moment(100,.3,30),15)
    def test_aligned_force(self):self.assertAlmostEqual(moment(100,.3,180),0)
    def test_angle_domain(self):
        with self.assertRaises(ValueError):moment(100,.3,181)
    def test_pressure_units(self):self.assertEqual(contact_pressure(200,100)['kpa'],20)
    def test_area_inverse(self):self.assertEqual(contact_pressure(200,200)['kpa'],10)
    def test_stress_units(self):self.assertEqual(normal_stress(100,50)['mpa'],2)
    def test_strain(self):self.assertEqual(engineering_strain(1,100),.01)
    def test_compression_strain(self):self.assertEqual(engineering_strain(-1,100),-.01)
    def test_zero_area(self):
        with self.assertRaises(ValueError):contact_pressure(100,0)
    def test_relaxation_initial(self):self.assertEqual(relaxation_analogy()['rows'][0]['value'],100)
    def test_relaxation_decay(self):self.assertGreater(relaxation_analogy()['rows'][0]['value'],relaxation_analogy()['rows'][-1]['value'])
    def test_relaxation_not_healing(self):self.assertIn('no human tissue',relaxation_analogy()['scope'])
    def test_relaxation_domain(self):
        for args in [(10,20,10),(100,40,0)]:
            with self.assertRaises(ValueError):relaxation_analogy(*args)
    def test_view_geometry(self):self.assertEqual(view_geometry(3,4)['distance_cm'],5)
    def test_view_negative_angle(self):self.assertLess(view_geometry()['angle_deg'],0)
    def test_visual_angle(self):self.assertGreater(angular_size(4,50)['degrees'],angular_size(4,100)['degrees'])
    def test_horizontal_work(self):self.assertEqual(horizontal_work()['joules'],500)
    def test_horizontal_power(self):self.assertEqual(horizontal_work()['watts'],50)
    def test_force_projection(self):self.assertAlmostEqual(horizontal_work(angle_deg=90)['joules'],0)
    def test_finite_bool_negative(self):
        for value in [True,-1,float('nan'),float('inf')]:
            with self.assertRaises(ValueError):mass_force(value)

class RNLETests(unittest.TestCase):
    def test_baseline(self):self.assertAlmostEqual(rnle()['rwl_kg'],23*.91*.94)
    def test_li(self):self.assertAlmostEqual(rnle()['li'],12/(23*.91*.94))
    def test_h_min_rule(self):self.assertEqual(rnle(h_cm=0)['factors']['HM'],1)
    def test_h_smaller_than_25(self):self.assertEqual(rnle(h_cm=20)['factors']['HM'],1)
    def test_h_farther(self):self.assertEqual(rnle(h_cm=50)['factors']['HM'],.5)
    def test_h_upper(self):self.assertAlmostEqual(rnle(h_cm=63)['factors']['HM'],25/63)
    def test_h_over_range(self):
        with self.assertRaises(ValueError):rnle(h_cm=63.1)
    def test_v_boundaries(self):
        self.assertAlmostEqual(rnle(v_cm=0)['factors']['VM'],.775);self.assertAlmostEqual(rnle(v_cm=175)['factors']['VM'],.7)
    def test_d_lower_rule(self):self.assertEqual(rnle(d_cm=0)['factors']['DM'],1)
    def test_a_boundary(self):self.assertAlmostEqual(rnle(a_deg=135)['factors']['AM'],.568)
    def test_geometry_rejection(self):
        for kwargs in [{'v_cm':176},{'d_cm':176},{'a_deg':136}]:
            with self.assertRaises(ValueError):rnle(**kwargs)
    def test_unknown_fm(self):self.assertIsNone(rnle(fm=None)['rwl_kg'])
    def test_unknown_cm(self):self.assertIsNone(rnle(cm=None)['li'])
    def test_unverified(self):self.assertIsNone(rnle(conditions_verified=False)['rwl_kg'])
    def test_zero_rwl_not_zero_li(self):
        result=rnle(fm=0);self.assertEqual(result['rwl_kg'],0);self.assertIsNone(result['li'])
    def test_bad_multipliers(self):
        for kwargs in [{'fm':1.1},{'cm':-1},{'fm':True},{'conditions_verified':1}]:
            with self.assertRaises(ValueError):rnle(**kwargs)
    def test_no_personal_capacity(self):self.assertIn('not full applicability',rnle()['scope'])

class ObservationTests(unittest.TestCase):
    def test_available(self):self.assertEqual(summarize([1,None,3])['available_mean'],2)
    def test_complete_unknown(self):self.assertIsNone(summarize([1,None,3])['complete_total'])
    def test_zero_known(self):self.assertEqual(summarize([0])['observed'],1)
    def test_empty_mean(self):self.assertIsNone(summarize([])['available_mean'])
    def test_original_scale(self):
        with self.assertRaises(ValueError):summarize([11],10)
    def test_repetition_rate(self):self.assertEqual(repetition()['actions_per_observed_minute'],9)
    def test_active_fraction(self):self.assertEqual(repetition()['active_fraction'],.7)
    def test_repetition_domain(self):
        for args in [(1.5,10,5),(100,0,0),(100,10,11)]:
            with self.assertRaises(ValueError):repetition(*args)
    def test_schedule(self):self.assertEqual(schedule()['total_minutes'],240)
    def test_schedule_empty(self):
        with self.assertRaises(ValueError):schedule(0,0,4)
    def test_geometry_sample(self):
        result=population_fit(workers());self.assertEqual(len(result['known_match_ids']),3);self.assertEqual(len(result['unknown_ids']),2)
    def test_known_sample_denominator(self):self.assertEqual(population_fit(workers())['known_fraction'],.3)
    def test_false_context_known(self):self.assertEqual(coverage({'checked':False},['checked'])['known'],['checked'])
    def test_missing_context(self):self.assertEqual(coverage({'a':None},['a','b'])['unknown'],['a','b'])
    def test_controls(self):self.assertIn('重新設計',control_example()['example'])
    def test_invalid_control(self):
        with self.assertRaises(ValueError):control_example('unrecognized')

class VibrationTests(unittest.TestCase):
    def test_single_segment(self):self.assertEqual(hav_a8([{'a_hv_m_s2':4,'trigger_minutes':120}])['complete_a8'],2)
    def test_multiple_segments(self):self.assertAlmostEqual(hav_a8([{'a_hv_m_s2':4,'trigger_minutes':120},{'a_hv_m_s2':2,'trigger_minutes':120}])['complete_a8'],math.sqrt(5))
    def test_missing_segment(self):self.assertIsNone(hav_a8([{'a_hv_m_s2':None,'trigger_minutes':120}])['complete_a8'])
    def test_incomplete_day(self):self.assertIsNone(hav_a8([{'a_hv_m_s2':4,'trigger_minutes':120}],False)['complete_a8'])
    def test_no_exposure_explicit(self):self.assertEqual(hav_a8([])['complete_a8'],0)
    def test_zero_known(self):self.assertEqual(hav_a8([{'a_hv_m_s2':0,'trigger_minutes':120}])['known_segments'],1)
    def test_negative(self):
        with self.assertRaises(ValueError):hav_a8([{'a_hv_m_s2':-1,'trigger_minutes':120}])
    def test_day_duration(self):
        with self.assertRaises(ValueError):hav_a8([{'a_hv_m_s2':1,'trigger_minutes':1441}])
    def test_unknown_amplitude_preserves_known_time(self):
        result=hav_a8([{'a_hv_m_s2':None,'trigger_minutes':120}])
        self.assertEqual(result['known_trigger_minutes'],120)
        self.assertEqual(result['known_segments'],0)
        self.assertIsNone(result['complete_a8'])
    def test_unknown_amplitude_cannot_hide_excess_time(self):
        with self.assertRaises(ValueError):hav_a8([{'a_hv_m_s2':None,'trigger_minutes':1441}])
    def test_total_time_includes_unknown_amplitude_segment(self):
        with self.assertRaises(ValueError):hav_a8([{'a_hv_m_s2':4,'trigger_minutes':1000},{'a_hv_m_s2':None,'trigger_minutes':500}])
    def test_not_wbv(self):self.assertIn('not raw phone',hav_a8([])['scope'])

class DataAndReportTests(unittest.TestCase):
    def changed_observations(self,change):
        with (DATA/'observations.csv').open(encoding='utf-8',newline='') as stream:rows=list(csv.DictReader(stream))
        change(rows)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'changed.csv'
            with p.open('w',encoding='utf-8',newline='') as stream:
                writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
            with self.assertRaises(ValueError):observations(p)
    def test_duplicate_slot(self):self.changed_observations(lambda rows:rows[1].update(id=rows[0]['id']))
    def test_status_mismatch(self):self.changed_observations(lambda rows:rows[0].update(status='missing'))
    def test_real_data_not_accepted(self):self.changed_observations(lambda rows:rows[0].update(synthetic='false'))
    def test_missing_slot(self):self.changed_observations(lambda rows:rows.pop())
    def test_task_windows(self):self.assertEqual(len(observations()),12)
    def test_observed_count(self):self.assertEqual(observation_summary()['observed_windows'],11)
    def test_observed_rate(self):self.assertEqual(observation_summary()['available_actions_per_minute'],9)
    def test_incomplete_rate_unknown(self):self.assertIsNone(observation_summary()['complete_actions_per_minute'])
    def test_lift_cases(self):self.assertEqual(len(lift_cases()),3)
    def test_svg_gap(self):self.assertIn('? = unobserved',observation_svg(observations()))
    def test_svg_finite(self):self.assertNotIn('NaN',observation_svg(observations()))
    def test_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'new';report=deliver(dest);self.assertTrue(all(report['checks'].values()));self.assertEqual(len(report['data_sha256']),5)
            self.assertEqual({p.name for p in dest.iterdir()},{'task_observations.csv','task_observations.svg','report.json'})
            saved=json.loads((dest/'report.json').read_text(encoding='utf-8'));self.assertIsNone(saved['observations']['complete_actions'])
    def test_existing_directory_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileExistsError):deliver(Path(tmp))

if __name__=='__main__':unittest.main()
