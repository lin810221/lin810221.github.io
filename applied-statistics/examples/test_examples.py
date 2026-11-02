"""Known-value, design-boundary and offline integration tests; synthetic data only."""
import contextlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
from scipy import stats
from course_core import (sample,counts,describe,mean_ci,proportion_ci,variance_ci,
    sample_size_mean,one_t,welch,paired,z_power,variance_test,variance_ratio,contingency,
    one_way,posthoc,factorial,regression,load_survey,alpha_reliability,factor_report,survey_report,save_report)

ROOT=Path(__file__).resolve().parent

class DescriptiveTests(unittest.TestCase):
    def test_01_hand_mean_variance(self):
        r=describe([2,4,6]);self.assertEqual(r['mean'],4);self.assertEqual(r['sample_variance'],4)
    def test_02_quartile_convention(self):
        r=describe([1,2,3,4]);self.assertEqual([r['q1'],r['median'],r['q3']],[1.75,2.5,3.25])
    def test_03_iqr_half(self):
        r=describe([2,4,6]);self.assertEqual(r['iqr'],2);self.assertEqual(r['quartile_deviation'],1)
    def test_04_mean_absolute_deviation(self):self.assertAlmostEqual(describe([2,4,6])['mean_absolute_deviation_about_mean'],4/3)
    def test_05_outlier_mean_and_median(self):
        a=describe([1,2,3,4,5]);b=describe([1,2,3,4,500]);self.assertEqual(a['median'],b['median']);self.assertGreater(b['mean'],a['mean']*10)
    def test_06_constant_descriptives(self):self.assertEqual(describe([3,3,3])['sample_sd'],0)
    def test_07_cv_invalid_origin(self):
        self.assertIsNone(describe([-2,-1,0],ratio_scale=True)['cv']);self.assertIsNone(describe([2,4,6])['cv']);self.assertEqual(describe([2,4,6],ratio_scale=True)['cv'],.5)
    def test_08_missing_not_silently_dropped(self):
        with self.assertRaises(ValueError):sample([1,np.nan,2])
    def test_09_wrong_shape(self):
        with self.assertRaises(ValueError):sample([[1,2],[3,4]])
    def test_10_insufficient_sample(self):
        with self.assertRaises(ValueError):sample([1])

class InferenceTests(unittest.TestCase):
    def test_11_known_sigma_margin(self):
        r=mean_ci([1,2,3,4],sigma=2);self.assertAlmostEqual(r['ci'][1]-r['estimate'],1.959963984540054,places=8)
    def test_12_unknown_sigma_se(self):self.assertAlmostEqual(mean_ci([2,4,6])['se'],2/math.sqrt(3))
    def test_13_ci_symmetric(self):
        r=mean_ci([1,3,5,8]);self.assertAlmostEqual(sum(r['ci'])/2,r['estimate'])
    def test_14_confidence_width(self):
        a=mean_ci([1,3,5,8],.90);b=mean_ci([1,3,5,8],.99);self.assertGreater(b['ci'][1]-b['ci'][0],a['ci'][1]-a['ci'][0])
    def test_15_wilson_zero_not_zero_width(self):
        ci=proportion_ci(0,10)['ci'];self.assertAlmostEqual(ci[0],0);self.assertGreater(ci[1],.25)
    def test_16_wilson_all_successes(self):
        ci=proportion_ci(10,10)['ci'];self.assertAlmostEqual(ci[1],1);self.assertLess(ci[0],.75)
    def test_17_exact_binomial_upper(self):self.assertAlmostEqual(proportion_ci(0,10,method='exact')['ci'][1],1-.025**.1)
    def test_18_count_validation(self):
        for k,n in [(2,1),(-1,5),(1.2,5),(1,0),(True,3)]:
            with self.subTest(k=k,n=n),self.assertRaises(ValueError):counts(k,n)
    def test_19_variance_interval_chi2_df2(self):
        ci=variance_ci([1,2,3])['ci'];self.assertAlmostEqual(ci[0],2/(-2*math.log(.025)));self.assertAlmostEqual(ci[1],2/(-2*math.log(.975)))
    def test_20_sample_size_rounds_up(self):self.assertEqual(sample_size_mean(10,2),97)
    def test_21_power_at_null_is_alpha(self):self.assertAlmostEqual(z_power(30,0),.05)
    def test_22_power_increases_with_n(self):self.assertGreater(z_power(100,.5),z_power(20,.5))
    def test_23_power_two_sided_symmetric(self):self.assertAlmostEqual(z_power(30,.5),z_power(30,-.5))
    def test_24_variance_pvalue_df2(self):self.assertAlmostEqual(variance_test([1,2,3],1)['p'],2/math.e)
    def test_25_invalid_intervals(self):
        for kwargs in [{'level':1},{'sigma':0},{'sigma':float('nan')}]:
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):mean_ci([1,2,3],**kwargs)

class ComparisonTests(unittest.TestCase):
    def test_26_welch_hand_calculation(self):
        r=welch([1,2,3],[3,5,7]);self.assertEqual(r['difference_A_minus_B'],-3);self.assertAlmostEqual(r['df'],50/17);self.assertAlmostEqual(r['t'],-3/math.sqrt(5/3))
    def test_27_welch_swap(self):
        a=welch([1,2,4],[2,4,6,7]);b=welch([2,4,6,7],[1,2,4]);self.assertAlmostEqual(a['p'],b['p']);self.assertAlmostEqual(a['t'],-b['t'])
    def test_28_paired_direction(self):
        r=paired([10,20,30,40],[11,22,34,43]);self.assertEqual(r['estimate'],2.5);self.assertAlmostEqual(r['t'],2.5/math.sqrt((5/3)/4))
    def test_29_unmatched_rejected(self):
        with self.assertRaises(ValueError):paired([1,2],[2,3,4])
    def test_30_zero_welch_se_rejected(self):
        with self.assertRaises(ValueError):welch([1,1],[2,2])
    def test_31_variance_ratio_scale(self):self.assertAlmostEqual(variance_ratio([2,4,6],[1,2,3])['F_A_over_B'],4)
    def test_32_chi_square_hand(self):
        r=contingency([[10,20],[20,10]]);self.assertAlmostEqual(r['chi2'],20/3);self.assertEqual(r['df'],1);self.assertAlmostEqual(r['cramers_v'],1/3)
    def test_33_chi_square_expected_margins(self):
        a=np.array([[4,6,10],[8,3,9]]);expected=contingency(a)['expected'];np.testing.assert_allclose(expected.sum(0),a.sum(0));np.testing.assert_allclose(expected.sum(1),a.sum(1))
    def test_34_zero_margin_rejected(self):
        with self.assertRaises(ValueError):contingency([[0,1],[0,2]])
    def test_35_anova_hand_sums(self):
        r=one_way([[1,2,3],[3,4,5],[5,6,7]]);self.assertEqual(r['classical_sums_of_squares'],{'between':24,'within':6,'total':30});self.assertAlmostEqual(r['F'],12)
    def test_36_two_group_anova_equals_t_squared(self):
        x=[1,2,4,5];y=[2,3,6,8];self.assertAlmostEqual(one_way([x,y])['F'],stats.ttest_ind(x,y,equal_var=True).statistic**2)
    def test_37_adjusted_pair_direction(self):
        r=posthoc([[1,2,3],[3,4,5],[5,6,7]]);np.testing.assert_allclose(r['differences'],[2,4,2]);self.assertEqual(r['pairs'],[['G1','G2'],['G1','G3'],['G2','G3']])
    def test_38_games_howell_finite(self):
        r=posthoc([[1,2,4],[2,4,8,9],[5,6,7]],'unequal');self.assertTrue(np.isfinite(r['adjusted_p']).all());self.assertTrue(((r['adjusted_p']>=0)&(r['adjusted_p']<=1)).all())
    def test_39_factorial_replicated_df(self):
        a=factorial(True);b=factorial(False);self.assertEqual(a['table']['Residual']['df'],42);self.assertEqual(b['table']['Residual']['df'],44);self.assertIn('C(A):C(B)',a['table'])
    def test_40_known_OLS_coefficients(self):
        x=np.array([-2,-1,0,1,2]);y=1+2*x+np.array([1,-2,2,-2,1]);r=regression(x,y);np.testing.assert_allclose(r['coefficients_intercept_slope'],[1,2]);self.assertAlmostEqual(r['r_squared'],20/27)

class QuestionnaireTests(unittest.TestCase):
    def setUp(self):self.data=load_survey()
    def test_41_unique_ids(self):self.assertEqual(len(self.data),180);self.assertTrue(self.data.id.is_unique)
    def test_42_reverse_scoring(self):np.testing.assert_allclose(self.data.q3+self.data.q3_negative,6)
    def test_43_score_requires_two_items(self):self.assertTrue(pd.isna(self.data.loc[3,'service']));self.assertEqual(self.data.service.notna().sum(),179)
    def test_44_complete_case_count(self):self.assertEqual(len(self.data[['q1','q2','q3']].dropna()),173)
    def test_45_identical_items_alpha_one(self):self.assertAlmostEqual(alpha_reliability(np.array([[1,1],[2,2],[4,4],[5,5]])),1)
    def test_46_reverse_scoring_improves_alpha(self):
        a=self.data[['q1','q2','q3']].dropna();b=self.data.loc[a.index,['q1','q2','q3_negative']];self.assertGreater(alpha_reliability(a),alpha_reliability(b))
    def test_47_alpha_rejects_implicit_missing(self):
        with self.assertRaises(ValueError):alpha_reliability(self.data[['q1','q2','q3']])
    def test_48_factor_shape_and_support(self):
        r=factor_report(self.data[['q1','q2','q3','q4','q5','q6']].dropna());self.assertEqual(r['n_complete'],170);self.assertEqual(r['loadings'].shape,(6,2));self.assertGreater(r['kmo'],0);self.assertLess(r['kmo'],1)
    def test_49_factor_does_not_modify_data(self):
        a=self.data[['q1','q2','q3','q4','q5','q6']].dropna().to_numpy();before=a.copy();factor_report(a);np.testing.assert_array_equal(a,before)
    def test_50_duplicate_id_rejected(self):
        data=pd.read_csv(ROOT/'data/survey.csv');data.loc[1,'id']=data.loc[0,'id']
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'invalid.csv';data.to_csv(p,index=False)
            with self.assertRaises(ValueError):load_survey(p)
    def test_51_out_of_scale_rejected(self):
        data=pd.read_csv(ROOT/'data/survey.csv');data.loc[0,'q1']=9
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'invalid.csv';data.to_csv(p,index=False)
            with self.assertRaises(ValueError):load_survey(p)
    def test_52_pairing_by_id_not_position(self):
        a=self.data[['id','before']].sample(frac=1,random_state=1);b=self.data[['id','after']].sample(frac=1,random_state=2);joined=a.merge(b,on='id',validate='one_to_one')
        self.assertAlmostEqual(paired(joined.before,joined.after)['estimate'],(self.data.after-self.data.before).mean())

class DeliveryTests(unittest.TestCase):
    def test_53_full_report_versions(self):
        r=survey_report();self.assertEqual(r['versions']['scipy'],'1.18.1');self.assertEqual(r['versions']['statsmodels'],'0.15.0')
    def test_54_report_saved_and_parsed(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'report.json';save_report(path,survey_report());r=json.loads(path.read_text(encoding='utf-8'));self.assertEqual(r['n_rows'],180);self.assertEqual(r['reliability']['n_complete'],173)
    def test_55_report_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'a.json';path.write_text('original',encoding='utf-8')
            with self.assertRaises(FileExistsError):save_report(path,{'a':1})
            self.assertEqual(path.read_text(encoding='utf-8'),'original')
    def test_56_nonfinite_report_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'a.json'
            with self.assertRaises(ValueError):save_report(path,{'a':float('nan')})
            self.assertFalse(path.exists())
    def test_57_prediction_interval_wider(self):
        r=regression()['prediction_at_mean_x'];self.assertGreater(r['obs_ci_upper']-r['obs_ci_lower'],r['mean_ci_upper']-r['mean_ci_lower'])
    def test_58_hc3_changes_se_not_coefficients(self):
        r=regression();self.assertTrue(np.isfinite(r['HC3_se']).all());self.assertFalse(np.allclose(r['classical_se'],r['HC3_se']))
    def test_59_constant_predictor_rejected(self):
        with self.assertRaises(ValueError):regression([1,1,1],[1,2,3])
    def test_60_all_entrypoints_offline_from_other_cwd(self):
        files=sorted(ROOT.glob('[0-9][0-9]_*.py'));self.assertEqual(len(files),40)
        def denied(*args,**kwargs):raise AssertionError('Examples must remain offline')
        original=Path.cwd()
        with tempfile.TemporaryDirectory() as folder,patch.object(socket.socket,'connect',denied),patch.object(socket,'create_connection',denied):
            try:
                os.chdir(folder)
                for path in files:
                    with self.subTest(example=path.name):
                        spec=importlib.util.spec_from_file_location(path.stem,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
                        with contextlib.redirect_stdout(io.StringIO()):report=module.main([])
                        self.assertIsInstance(report,dict);json.dumps(report,allow_nan=False)
            finally:os.chdir(original)

if __name__=='__main__':unittest.main()
