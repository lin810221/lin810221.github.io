"""Numerical and semantic contracts for non-diagnostic educational examples."""
import csv,json,math,tempfile,unittest
from copy import deepcopy
from pathlib import Path
from metabolic_core import *
from metabolic_data import DATA,bp_readings,bp_summary,visits,visit_arithmetic
from reporting import deliver,bp_svg

class UnitTests(unittest.TestCase):
    def test_glucose(self):self.assertEqual(concentration(126),7)
    def test_cholesterol(self):self.assertAlmostEqual(concentration(38.67,'cholesterol'),1)
    def test_triglycerides(self):self.assertAlmostEqual(concentration(88.57,'triglycerides'),1)
    def test_creatinine(self):self.assertAlmostEqual(concentration(1,'creatinine','mg/dL','umol/L'),88.4)
    def test_roundtrips(self):
        for analyte,other in [('glucose','mmol/L'),('cholesterol','mmol/L'),('triglycerides','mmol/L'),('creatinine','umol/L')]:
            self.assertAlmostEqual(concentration(concentration(100,analyte,'mg/dL',other),analyte,other,'mg/dL'),100)
    def test_analyte_required(self):
        for analyte in ['lipids','lp_a','insulin']:
            with self.assertRaises(ValueError):concentration(100,analyte)
    def test_units_not_silently_reused(self):
        with self.assertRaises(ValueError):concentration(1,'creatinine','mg/dL','mmol/L')
    def test_a1c_equation(self):self.assertAlmostEqual(a1c_units(48,'IFCC_mmol_mol')['ngsp_percent'],6.54304)
    def test_a1c_roundtrip(self):self.assertAlmostEqual(a1c_units(a1c_units(6.5)['ifcc_mmol_mol'],'IFCC_mmol_mol')['ngsp_percent'],6.5)
    def test_a1c_not_glucose(self):
        with self.assertRaises(ValueError):a1c_units(48,'mmol/L')
    def test_negative_inverse_rejected(self):
        with self.assertRaises(ValueError):a1c_units(1)
    def test_nonfinite_bool_negative(self):
        for value in [True,False,-1,float('nan'),float('inf')]:
            with self.assertRaises(ValueError):nonnegative(value=value)

class ArithmeticTests(unittest.TestCase):
    def test_bmi(self):self.assertAlmostEqual(bmi(70,1.7),70/2.89)
    def test_bmi_zero_height(self):
        with self.assertRaises(ValueError):bmi(70,0)
    def test_waist_ratio(self):self.assertEqual(waist_height(85,170),.5)
    def test_change(self):self.assertEqual(change(80,76)['relative_percent'],-5)
    def test_zero_baseline(self):self.assertIsNone(change(0,1)['relative_percent'])
    def test_non_hdl(self):self.assertEqual(non_hdl(200,50),150)
    def test_non_hdl_molar(self):self.assertAlmostEqual(non_hdl(5.2,1.3,'mmol/L'),3.9)
    def test_impossible_lipid_subset(self):
        with self.assertRaises(ValueError):non_hdl(40,50)
    def test_friedewald_historical(self):self.assertEqual(friedewald(200,50,150)['ldl_estimate'],120)
    def test_friedewald_boundary(self):self.assertIsNone(friedewald(200,50,400)['ldl_estimate'])
    def test_friedewald_context(self):self.assertIsNone(friedewald(200,50,150,fasting=False)['ldl_estimate'])
    def test_friedewald_negative_not_zero(self):self.assertIsNone(friedewald(50,45,100)['ldl_estimate'])
    def test_homa(self):self.assertAlmostEqual(homa_ir(8,100)['homa1_ir'],800/405)
    def test_homa_context(self):self.assertIsNone(homa_ir(8,100,False)['homa1_ir'])
    def test_homa_scope(self):self.assertIn('not HOMA2',homa_ir()['scope'])
    def test_fib4(self):self.assertAlmostEqual(fib4()['fib4'],45*25/(220*math.sqrt(30)))
    def test_fib4_not_stable(self):self.assertIsNone(fib4(stable_adult=False)['fib4'])
    def test_fib4_domain(self):
        for args in [(17,25,30,220),(45,25,0,220),(45,25,30,0)]:
            with self.assertRaises(ValueError):fib4(*args)
    def test_urine_acr(self):self.assertEqual(urine_acr(20,1)['acr_mg_g'],20)
    def test_urine_zero_denominator(self):
        with self.assertRaises(ValueError):urine_acr(20,0)
    def test_bsa(self):self.assertAlmostEqual(body_surface_area(170,70),math.sqrt(11900/3600))
    def test_gfr_indexing(self):self.assertEqual(unindex_gfr(90,1.73)['absolute_ml_min'],90)
    def test_gfr_not_drug_dose(self):self.assertIn('not measured GFR',unindex_gfr()['scope'])

class EvidenceTests(unittest.TestCase):
    def test_risk_rr_arr(self):
        r=risk_comparison();self.assertAlmostEqual(r['rr'],.8);self.assertAlmostEqual(r['absolute_reduction'],.02);self.assertAlmostEqual(r['number_needed_exact'],50)
    def test_risk_harm(self):self.assertEqual(risk_comparison(20,100,10,100)['direction'],'harm')
    def test_risk_zero_control(self):self.assertIsNone(risk_comparison(1,100,0,100)['rr'])
    def test_risk_no_difference(self):self.assertIsNone(risk_comparison(1,100,1,100)['number_needed_exact'])
    def test_risk_counts(self):
        for args in [(101,100,1,100),(1.5,100,1,100),(True,100,1,100),(1,0,1,100)]:
            with self.assertRaises(ValueError):risk_comparison(*args)
    def test_baseline_effect(self):
        self.assertAlmostEqual(assumed_effect(.1,.8)['absolute_reduction'],.02);self.assertAlmostEqual(assumed_effect(.01,.8)['absolute_reduction'],.002)
    def test_probability_limit(self):
        with self.assertRaises(ValueError):assumed_effect(.9,2)
    def test_screening_counts(self):
        r=screening();self.assertAlmostEqual(r['tp'],90);self.assertAlmostEqual(r['fp'],495);self.assertAlmostEqual(r['ppv'],90/585)
    def test_screening_total(self):
        r=screening();self.assertAlmostEqual(sum(r[k] for k in ('tp','fp','tn','fn')),10000)
    def test_prevalence_changes_ppv(self):self.assertGreater(screening(prevalence=.1)['ppv'],screening(prevalence=.01)['ppv'])
    def test_no_positive_results(self):self.assertIsNone(screening(prevalence=0,specificity=1)['ppv'])
    def test_invalid_screening_inputs(self):
        for kwargs in [{'population':0},{'sensitivity':1.1},{'specificity':-1},{'prevalence':float('nan')}]:
            with self.assertRaises(ValueError):screening(**kwargs)
    def test_prevent_ten_year_ages(self):
        self.assertTrue(prevent_age_scope(30,10)['age_range_match']);self.assertTrue(prevent_age_scope(79,10)['age_range_match']);self.assertFalse(prevent_age_scope(80,10)['age_range_match'])
    def test_prevent_thirty_year_ages(self):
        self.assertTrue(prevent_age_scope(59,30)['age_range_match']);self.assertFalse(prevent_age_scope(60,30)['age_range_match'])
    def test_prevent_scope_not_eligibility(self):self.assertIn('no full clinical eligibility',prevent_age_scope()['scope'])
    def test_prevent_input(self):
        with self.assertRaises(ValueError):prevent_age_scope(45.5)
    def test_false_is_known(self):self.assertEqual(coverage({'symptoms':False},['symptoms'])['known'],['symptoms'])
    def test_none_is_unknown(self):self.assertEqual(coverage({'symptoms':None},['symptoms'])['missing'],['symptoms'])
    def test_describe_missing(self):
        r=describe([100,None,110]);self.assertEqual(r['available_mean'],105);self.assertIsNone(r['complete_mean'])
    def test_all_missing(self):self.assertIsNone(describe([None])['available_mean'])
    def test_rolling(self):self.assertEqual(rolling([1,2,None,4,5],2),[None,1.5,None,None,4.5])
    def test_toy_zero(self):self.assertEqual(toy_balance(0)['rows'][-1]['state_arbitrary'],0)
    def test_toy_no_clearance(self):self.assertEqual(toy_balance(4,0,10)['rows'][-1]['state_arbitrary'],20)
    def test_toy_decay(self):
        rows=toy_balance()['rows'];self.assertLess(rows[-1]['state_arbitrary'],rows[4]['state_arbitrary'])
    def test_toy_scope(self):self.assertIn('not glucose',toy_balance()['scope'])

class DataTests(unittest.TestCase):
    def test_bp_slots(self):self.assertEqual(len(bp_readings()),28)
    def test_bp_completeness(self):
        r=bp_summary();self.assertEqual(r['observed_pairs'],27);self.assertEqual(r['expected_pairs'],28);self.assertIsNone(r['complete_mean'])
    def test_bp_available_mean(self):
        rows=[r for r in bp_readings() if r['sbp'] is not None];self.assertAlmostEqual(bp_summary()['available_mean']['sbp'],sum(r['sbp'] for r in rows)/27)
    def test_bp_exclusion_explicit(self):
        r=bp_summary(exclude_first_day=True);self.assertEqual(r['expected_pairs'],24);self.assertEqual(r['observed_pairs'],23);self.assertTrue(r['exclude_first_day'])
    def test_bp_complete_after_filling(self):
        rows=deepcopy(bp_readings());rows[-1].update(sbp=129,dbp=76);self.assertIsNotNone(bp_summary(rows)['complete_mean'])
    def test_missing_slot_not_removed(self):
        with self.assertRaises(ValueError):bp_summary(bp_readings()[:-1])
    def test_bp_duplicate(self):
        rows=bp_readings();rows[-1]=deepcopy(rows[0])
        with self.assertRaises(ValueError):bp_summary(rows)
    def test_bp_pair_integrity(self):
        rows=bp_readings();rows[-1]['sbp']=130
        with self.assertRaises(ValueError):bp_summary(rows)
    def test_bp_invalid_quality_not_counted(self):
        rows=bp_readings();rows[0]['quality']='invalid';self.assertEqual(bp_summary(rows)['observed_pairs'],26)
    def test_visits(self):self.assertEqual(len(visits()),4)
    def test_missing_lipid_propagation(self):self.assertIsNone(visit_arithmetic(visits()[2])['non_hdl_mg_dl'])
    def test_typed_units(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows=visits();rows[0]['labs']['glucose']['unit']='mmol/L';p=Path(tmp)/'bad.json';p.write_text(json.dumps(rows),encoding='utf-8')
            with self.assertRaises(ValueError):visits(p)
    def test_svg_no_diagnosis_line(self):self.assertIn('No diagnostic threshold',bp_svg(bp_summary()))
    def test_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'new-report';r=deliver(dest);self.assertTrue(all(r['checks'].values()))
            data=json.loads((dest/'report.json').read_text(encoding='utf-8'));self.assertEqual(len(data['data_sha256']),5);self.assertTrue(data['synthetic'])
            with (dest/'observations.csv').open(encoding='utf-8') as stream:rows=list(csv.DictReader(stream))
            self.assertEqual(rows[2]['non_hdl_mg_dl'],'');self.assertTrue((dest/'bp_observations.svg').is_file())
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileExistsError):deliver(Path(tmp))

if __name__=='__main__':unittest.main()
