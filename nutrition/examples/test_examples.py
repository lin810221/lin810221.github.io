"""Numerical, provenance and unknown-value acceptance. No health diagnoses or network."""
from pathlib import Path
from tempfile import TemporaryDirectory
from copy import deepcopy
from xml.etree import ElementTree
import json
import unittest
from nutrition_core import (mass,sodium_salt,energy,portion,serving_label,volume_mass,energy_percent,
    glycemic_load,vitamin_d,vitamin_a_rae,folate_dfe,reference_percent,scoped_total,rounded_interval,
    density_per_100kcal,match_energy,cooking,repeated_days,interval_sum,risk_comparison)
from food_data import foods,food_portion,meal,diary,references,free_sugar_known,DATA
from reporting import deliver,svg_diary


class UnitEnergyTests(unittest.TestCase):
    def test_g_mg_ug(self):
        self.assertAlmostEqual(mass(1000,'mg','g'),1);self.assertAlmostEqual(mass(1,'mg','ug'),1000)
    def test_roundtrip_mass(self):
        for a in ('g','mg','ug'):
            for b in ('g','mg','ug'):self.assertAlmostEqual(mass(mass(2,a,b),b,a),2)
    def test_no_generic_iu(self):
        with self.assertRaises(ValueError):mass(400,'IU','ug')
    def test_unit_domains(self):
        for value in (-1,True,float('nan'),float('inf')):
            with self.subTest(value=value),self.assertRaises(ValueError):mass(value)
    def test_salt_approximation(self):
        self.assertEqual(sodium_salt(2000)['salt_equivalent_g_approx'],5)
    def test_energy_components(self):
        r=energy();self.assertEqual(r['kcal'],380);self.assertAlmostEqual(r['kJ'],1589.92)
    def test_energy_adds_and_percent(self):
        r=energy(alcohol_g=10);self.assertEqual(sum(r['parts_kcal'].values()),r['kcal']);self.assertAlmostEqual(sum(r['percent_energy'].values()),100)
    def test_fiber_not_double_counted(self):
        self.assertEqual(energy(50,20,10,5)['kcal']-energy(50,20,10,0)['kcal'],10)
    def test_zero_energy_percent_unknown(self):
        self.assertTrue(all(v is None for v in energy(0,0,0,0)['percent_energy'].values()))
    def test_negative_energy_input(self):
        with self.assertRaises(ValueError):energy(fat_g=-1)
    def test_portion_linear(self):
        self.assertEqual(portion(12,250),30);self.assertEqual(portion(12,0),0)
    def test_portion_basis_positive(self):
        with self.assertRaises(ValueError):portion(10,20,0)
    def test_serving_vs_package(self):
        r=serving_label(120,250,500,500);self.assertEqual(r['amount_eaten'],240);self.assertEqual(r['servings_per_package'],2);self.assertEqual(r['per_100'],48)
    def test_no_unknown_density_conversion(self):
        with self.assertRaises(ValueError):volume_mass(240,'mL','g')
    def test_density_roundtrip(self):
        self.assertAlmostEqual(volume_mass(volume_mass(240,'mL','g',1.02),'g','mL',1.02),240)
    def test_same_unit_no_density(self):
        self.assertEqual(volume_mass(100,'g','g'),100)
    def test_fat_percent_energy(self):
        self.assertEqual(energy_percent(20,9,2000),9)
    def test_gl_not_from_total_sugar(self):
        self.assertEqual(glycemic_load(55,30),16.5);self.assertIsNone(glycemic_load(None,30))


class ReferenceTests(unittest.TestCase):
    def test_vitamin_d_conversion(self):
        self.assertEqual(vitamin_d(1000)['ug'],25);self.assertEqual(vitamin_d(25,'ug')['IU'],1000)
    def test_a_source_specific_factors(self):
        self.assertEqual(vitamin_a_rae(beta_food_ug=1200)['total_rae_ug'],100)
        self.assertEqual(vitamin_a_rae(beta_supp_ug=1200)['total_rae_ug'],600)
    def test_a_ul_preformed_separate(self):
        r=vitamin_a_rae(retinol_ug=300,beta_food_ug=1200);self.assertEqual(r['total_rae_ug'],400);self.assertEqual(r['preformed_retinol_ug'],300)
    def test_folate_food(self):
        r=folate_dfe(200);self.assertEqual(r['dfe_ug'],200);self.assertEqual(r['synthetic_folic_acid_ug'],0)
    def test_folate_with_food(self):
        self.assertAlmostEqual(folate_dfe(240,'folic_acid_with_food')['dfe_ug'],400)
    def test_folate_empty_stomach(self):
        self.assertEqual(folate_dfe(200,'folic_acid_empty_stomach')['dfe_ug'],400)
    def test_unknown_mthf_rejected(self):
        with self.assertRaises(ValueError):folate_dfe(200,'5-MTHF')
    def test_nrv_sodium(self):
        self.assertEqual(reference_percent(400,'mg',references()['tw_label_sodium'])['percent'],20)
    def test_nrv_converts_mass(self):
        self.assertEqual(reference_percent(.4,'g',references()['tw_label_sodium'])['percent'],20)
    def test_no_sugar_nrv_invented(self):
        self.assertIsNone(reference_percent(10,'g',references()['tw_label_sugars'])['percent'])
    def test_no_trans_nrv_invented(self):
        self.assertIsNone(references()['tw_label_trans_fat']['value'])
    def test_units_mismatch(self):
        with self.assertRaises(ValueError):reference_percent(1,'kcal',references()['tw_label_sodium'])
    def test_folate_ul_requires_form_and_scope(self):
        r=references()['us_folic_acid_ul']
        with self.assertRaises(ValueError):reference_percent(400,'ug',r)
        with self.assertRaises(ValueError):reference_percent(400,'ug',r,form='DFE',source_scope='supplements_and_fortification')
        self.assertEqual(reference_percent(400,'ug',r,form='folic_acid',source_scope='supplements_and_fortification')['percent'],40)
    def test_missing_source_metadata(self):
        r=references()['tw_label_sodium'];del r['source']
        with self.assertRaises(ValueError):reference_percent(400,'mg',r)
    def test_scoped_exclusion(self):
        rows=[{'amount':400,'source_type':'supplement'},{'amount':1000,'source_type':'natural_food'}]
        self.assertEqual(scoped_total(rows,{'supplement'})['amount'],400)
    def test_scoped_missing_propagates(self):
        r=scoped_total([{'name':'unknown supplement','amount':None,'source_type':'supplement'}],{'supplement'})
        self.assertIsNone(r['amount']);self.assertEqual(r['missing'],['unknown supplement'])
    def test_excluded_missing_does_not_poison(self):
        self.assertEqual(scoped_total([{'amount':None,'source_type':'natural_food'}],{'supplement'})['amount'],0)
    def test_rounding_zero_not_absence(self):
        r=rounded_interval();self.assertEqual(r['lower'],0);self.assertEqual(r['upper_exclusive'],.05);self.assertIn('not a legal',r['scope'])


class DataTests(unittest.TestCase):
    def test_fixture_provenance_and_count(self):
        self.assertEqual(len(foods()),10);self.assertTrue(all(f['source_type']=='synthetic' for f in foods().values()))
    def test_nutrient_subsets(self):
        for f in foods().values():
            r=f['nutrients'];self.assertLessEqual(r['saturated_g'],r['fat_g']);self.assertLessEqual(r['total_sugars_g'],r['available_carb_g'])
    def test_amount_scaling(self):
        r=food_portion(foods()['milk'],240,'mL');self.assertAlmostEqual(r['nutrients']['calcium_mg'],264)
    def test_food_volume_needs_density(self):
        with self.assertRaises(ValueError):food_portion(foods()['milk'],240,'g')
    def test_food_explicit_density(self):
        f=foods()['soy'];self.assertAlmostEqual(food_portion(f,244.8,'g')['nutrients']['protein_g'],7.2)
    def test_zero_missing_food_contributes_zero(self):
        self.assertEqual(food_portion(foods()['drink'],0)['nutrients']['calcium_mg'],0)
    def test_missing_food_not_zero(self):
        self.assertIsNone(food_portion(foods()['drink'],100)['nutrients']['calcium_mg'])
    def test_meal_known_subtotal_preserved(self):
        r=meal([{'food_id':'milk','amount':240},{'food_id':'drink','amount':330}])['nutrients']['calcium_mg']
        self.assertIsNone(r['amount']);self.assertAlmostEqual(r['known_subtotal'],264);self.assertEqual(r['missing_foods'],['drink'])
    def test_meal_splitting_invariance(self):
        a=meal([{'food_id':'grain','amount':200}]);b=meal([{'food_id':'grain','amount':100},{'food_id':'grain','amount':100}])
        self.assertEqual(a['nutrients'],b['nutrients'])
    def test_missing_one_nutrient_not_all(self):
        r=meal([{'food_id':'drink','amount':330}])['nutrients'];self.assertEqual(r['energy_kcal']['amount'],132);self.assertIsNone(r['calcium_mg']['amount'])
    def test_unknown_id_rejected(self):
        with self.assertRaises(ValueError):meal([{'food_id':'nonexistent','amount':1}])
    def test_sugar_not_inferred(self):
        self.assertIsNone(free_sugar_known(foods()['soy'])['value']);self.assertEqual(free_sugar_known(foods()['fruit'])['value'],0)
    def test_diary_recorded_days(self):
        r=diary();self.assertEqual(len(r),3);self.assertIsNone(r['day3']['nutrients']['calcium_mg']['amount'])
    def test_six_food_groups_not_adequacy_score(self):
        r=meal([{'food_id':'fruit','amount':0},{'food_id':'grain','amount':1}]);self.assertEqual(r['groups_present'],['whole_grains']);self.assertIn('does not establish',r['interpretation'])
    def test_metadata_references_explicit(self):
        for ref in references().values():self.assertTrue(ref['source'].startswith('https://'));self.assertTrue(ref['population']);self.assertEqual(ref['checked'],'2026-11-09')


class AssessmentEvidenceTests(unittest.TestCase):
    def test_density_denominator(self):
        self.assertEqual(density_per_100kcal(300,200),150)
        with self.assertRaises(ValueError):density_per_100kcal(300,0)
    def test_isoenergy_amount(self):
        self.assertAlmostEqual(match_energy(120,600),20)
    def test_cooking_water_dilution(self):
        r=cooking(100,250,8);self.assertEqual(r['retained_total'],8);self.assertEqual(r['per_100_cooked'],3.2)
    def test_cooking_retention(self):
        self.assertAlmostEqual(cooking(100,250,8,.8)['retained_total'],6.4)
    def test_cooking_invalid(self):
        with self.assertRaises(ValueError):cooking(100,0,8)
        with self.assertRaises(ValueError):cooking(100,100,8,1.1)
    def test_repeated_days(self):
        r=repeated_days([10,20,30]);self.assertEqual(r['mean'],20);self.assertEqual(r['sample_sd'],10)
    def test_one_day_no_variance(self):
        self.assertIsNone(repeated_days([10])['sample_sd'])
    def test_missing_day_not_zero(self):
        self.assertIsNone(repeated_days([10,None,30])['mean'])
    def test_interval_bounds(self):
        r=interval_sum([100,200],[(10,20),(20,40)]);self.assertEqual(r['lower'],50);self.assertEqual(r['upper'],100)
    def test_interval_unknown(self):
        self.assertIsNone(interval_sum([None],[(10,20)])['upper'])
    def test_invalid_interval(self):
        with self.assertRaises(ValueError):interval_sum([100],[(20,10)])
    def test_absolute_relative_risk(self):
        r=risk_comparison(1,100,2,100);self.assertEqual(r['relative_reduction'],.5);self.assertEqual(r['absolute_reduction'],.01);self.assertEqual(r['number_needed_exact'],100)
    def test_same_relative_different_absolute(self):
        a=risk_comparison(1,100,2,100);b=risk_comparison(100,1000,200,1000)
        self.assertEqual(a['relative_reduction'],b['relative_reduction']);self.assertNotEqual(a['absolute_reduction'],b['absolute_reduction'])
    def test_zero_control_risk(self):
        r=risk_comparison(0,100,0,100);self.assertIsNone(r['risk_ratio']);self.assertIsNone(r['number_needed_exact'])
    def test_harm_not_benefit(self):
        self.assertEqual(risk_comparison(2,100,1,100)['direction'],'harm')
    def test_invalid_risk_counts(self):
        with self.assertRaises(ValueError):risk_comparison(101,100,1,100)


class DeliveryTests(unittest.TestCase):
    def test_svg_valid_and_honest(self):
        svg=svg_diary(diary());self.assertEqual(ElementTree.fromstring(svg).tag,'{http://www.w3.org/2000/svg}svg');self.assertIn('not daily targets',svg)
    def test_complete_report(self):
        with TemporaryDirectory() as folder:
            out=Path(folder)/'report';deliver(out)
            r=json.loads((out/'report.json').read_text(encoding='utf-8'))
            self.assertTrue(r['synthetic']);self.assertTrue(all(r['checks'].values()));self.assertEqual(r['recorded_days'],3)
            self.assertIsNone(r['days']['day3']['nutrients']['calcium_mg']['amount']);self.assertEqual(len(r['data_sha256']),4)
            self.assertTrue((out/'recorded_intake.svg').is_file());self.assertTrue((out/'recorded_nutrients.csv').is_file())
            with self.assertRaises(FileExistsError):deliver(out)


if __name__=='__main__':unittest.main(verbosity=2)
