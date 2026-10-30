"""Numerical and pipeline integration tests on synthetic data; no network."""
import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch
import warnings

import numpy as np
import sklearn
from sklearn.base import clone
from sklearn.cluster import DBSCAN,KMeans
from sklearn.datasets import make_blobs
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.metrics import adjusted_rand_score
from sklearn.model_selection import GroupKFold,StratifiedKFold,TimeSeriesSplit,cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from threadpoolctl import threadpool_limits
import course_core as c

ROOT=Path(__file__).resolve().parent

def entry(number):
    path=next(ROOT.glob(f'{number:02d}_*.py'))
    spec=importlib.util.spec_from_file_location(f'ml_example_{number}',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DataTests(unittest.TestCase):
    def test_verified_framework_version(self):
        self.assertEqual(sklearn.__version__,'1.9.1')

    def test_split_coverage_and_disjoint(self):
        _,y=c.binary_data()
        parts=c.split_indices(y)
        self.assertEqual([len(parts[k]) for k in ('train','validation','test')],[180,60,60])
        sets=[set(v) for v in parts.values()]
        self.assertEqual(set.union(*sets),set(range(300)))
        self.assertFalse(sets[0]&sets[1] or sets[0]&sets[2] or sets[1]&sets[2])

    def test_split_stratification(self):
        _,y=c.binary_data()
        for indices in c.split_indices(y).values():
            self.assertLess(abs(y[indices].mean()-y.mean()),.02)

    def test_split_seed_reproducible(self):
        _,y=c.binary_data()
        a,b=c.split_indices(y),c.split_indices(y)
        for key in a:
            np.testing.assert_array_equal(a[key],b[key])

    def test_group_separation(self):
        groups=np.repeat(np.arange(12),3)
        for a,b in GroupKFold(3).split(np.zeros((36,1)),groups=groups):
            self.assertFalse(set(groups[a])&set(groups[b]))

    def test_time_order_and_gap(self):
        for a,b in TimeSeriesSplit(3,gap=2).split(np.arange(30)):
            self.assertLess(a[-1]+2,b[0])

    def test_train_only_imputer_statistics(self):
        train=np.array([[1.,2.],[3.,np.nan],[5.,6.]])
        p=make_pipeline(SimpleImputer(strategy='median'),StandardScaler()).fit(train)
        before=p[0].statistics_.copy()
        p.transform([[1000.,np.nan]])
        np.testing.assert_array_equal(before,[3.,4.])
        np.testing.assert_array_equal(before,p[0].statistics_)
        np.testing.assert_allclose(p[1].mean_,[3.,4.])

    def test_unknown_category_no_refit(self):
        encoder=OneHotEncoder(handle_unknown='ignore',sparse_output=False).fit([['a'],['b']])
        np.testing.assert_array_equal(encoder.transform([['new']]),[[0.,0.]])
        self.assertEqual(list(encoder.categories_[0]),['a','b'])

    def test_fold_specific_preprocessing(self):
        x,y=c.binary_data(n=90)
        folds=list(StratifiedKFold(3,shuffle=True,random_state=7).split(x,y))
        model=make_pipeline(StandardScaler(),LogisticRegression(l1_ratio=0,max_iter=1000))
        result=cross_validate(model,x,y,cv=folds,return_estimator=True)
        for (train,_),fitted in zip(folds,result['estimator']):
            np.testing.assert_allclose(fitted[0].mean_,x[train].mean(0))

    def test_mixed_pipeline_finite_and_unknown(self):
        x,y=c.make_mixed_data()
        model=c.mixed_pipeline().fit(x,y)
        values=c.records_to_array(c.sample_records())
        transformed=model[0].transform(values)
        self.assertTrue(np.isfinite(transformed).all())
        self.assertEqual(model.predict(values).shape,(3,))


class MetricTests(unittest.TestCase):
    def test_hand_confusion_and_f1(self):
        report=c.binary_metrics([1,1,0,0],[.9,.4,.8,.1])
        self.assertEqual([report[k] for k in ('tp','fp','fn','tn')],[1,1,1,1])
        self.assertEqual(report['precision'],.5)
        self.assertEqual(report['recall'],.5)
        self.assertEqual(report['f1'],.5)

    def test_zero_positive_predictions(self):
        report=c.binary_metrics([1,0],[.2,.1],.9)
        self.assertEqual(report['precision'],0)
        self.assertEqual(report['recall'],0)

    def test_single_class_auc_undefined(self):
        report=c.binary_metrics([0,0],[.2,.1])
        self.assertIsNone(report['roc_auc'])
        self.assertIsNone(report['average_precision'])

    def test_reject_nonprobability_scores(self):
        for scores in ([float('nan'),.2],[1.1,.2],[-.1,.2]):
            with self.assertRaises(ValueError):
                c.binary_metrics([1,0],scores)

    def test_reject_shapes_and_nonbinary(self):
        for y,scores in [([1],[.2,.3]),([2,0],[.2,.3]),([],[])]:
            with self.assertRaises(ValueError):
                c.binary_metrics(y,scores)

    def test_brier_manual(self):
        report=c.binary_metrics([1,0],[.8,.3])
        self.assertAlmostEqual(report['brier'],(.04+.09)/2)

    def test_threshold_equality_is_positive(self):
        self.assertEqual(c.binary_metrics([1,0],[.5,.49],.5)['tp'],1)

    def test_rmse_hand_and_negative_r2(self):
        report=c.regression_metrics([1,2,3],[1,2,5])
        self.assertAlmostEqual(report['mae'],2/3)
        self.assertAlmostEqual(report['rmse'],np.sqrt(4/3))
        self.assertLess(c.regression_metrics([1,2,3],[10,10,10])['r2'],0)

    def test_regression_shape_rejected(self):
        with self.assertRaises(ValueError):
            c.regression_metrics([1,2],[[1],[2]])

    def test_threshold_cost_optimal_on_validation(self):
        y=np.array([1,1,0,0]);p=np.array([.9,.4,.8,.1])
        selected=c.select_threshold(y,p,5,1)
        self.assertEqual(selected['validation_cost'],1)
        self.assertEqual(selected['threshold'],.4)

    def test_threshold_can_reject_score_one(self):
        selected=c.select_threshold([0,0],[1.,.9],0,1)
        self.assertGreater(selected['threshold'],1.)
        self.assertEqual(selected['validation_cost'],0)

    def test_invalid_cost_rejected(self):
        with self.assertRaises(ValueError):
            c.select_threshold([1,0],[.9,.1],-1,1)

    def test_probability_uses_class_order(self):
        class Model:
            classes_=np.array([1,0])
            def predict_proba(self,x):
                return np.array([[.8,.2]])
        np.testing.assert_array_equal(c.probability(Model(),[[1]]),[.8])
        with self.assertRaises(ValueError):
            c.probability(Model(),[[1]],positive=3)


class AlgorithmTests(unittest.TestCase):
    def test_linear_recovers_known_rule(self):
        x=np.arange(10.).reshape(-1,1);y=3*x[:,0]+.5
        m=LinearRegression().fit(x,y)
        np.testing.assert_allclose(m.coef_,[3.])
        self.assertAlmostEqual(m.intercept_,.5)

    def test_current_logistic_api(self):
        x,y=c.binary_data()
        m=make_pipeline(StandardScaler(),LogisticRegression(C=1.,l1_ratio=0,max_iter=1000)).fit(x,y)
        np.testing.assert_allclose(m.predict_proba(x).sum(1),np.ones(len(x)))

    def test_kmeans_label_permutation(self):
        x,truth=make_blobs(n_samples=90,centers=[[-3,-2],[0,3],[3,-2]],cluster_std=.4,random_state=7)
        labels=KMeans(n_clusters=3,n_init=10,random_state=7).fit_predict(x)
        self.assertAlmostEqual(adjusted_rand_score(truth,labels),1)
        self.assertEqual(adjusted_rand_score(labels,(labels+1)%3),1)

    def test_dbscan_isolated_point(self):
        x,_=make_blobs(n_samples=60,centers=[[-2,0],[2,0]],cluster_std=.2,random_state=7)
        labels=DBSCAN(eps=.6,min_samples=4).fit_predict(np.vstack([x,[[10.,10.]]]))
        self.assertEqual(labels[-1],-1)

    def test_pca_projection_reconstruction(self):
        t=np.linspace(-2,2,40);x=np.c_[t,2*t,-t]
        m=PCA(1).fit(x)
        np.testing.assert_allclose(m.inverse_transform(m.transform(x)),x,atol=1e-12)
        self.assertAlmostEqual(m.explained_variance_ratio_[0],1)

    def test_isolation_forest_score_direction(self):
        rng=np.random.default_rng(7)
        m=IsolationForest(n_estimators=50,random_state=7).fit(rng.normal(0,.4,(120,2)))
        scores=m.decision_function([[0.,0.],[8.,8.]])
        self.assertGreater(scores[0],scores[1])

    def test_permutation_importance_signal(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result=entry(28).main([])
        self.assertEqual(int(np.argmax(result['mean_score_drop'])),0)

    def test_calibration_actual_estimator(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result=entry(21).main([])
        self.assertEqual(result['calibrated_members'],3)
        self.assertTrue(np.isfinite(result['holdout']['log_loss']))

    def test_threshold_cv_actual_estimator(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result=entry(22).main([])
        self.assertTrue(0<=result['selected_threshold']<=1)


class ArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project=c.experiment()

    def test_full_project_separated_roles(self):
        self.assertEqual(self.project['split_sizes'],{'train':240,'validation':80,'test':80})
        self.assertEqual(self.project['test']['samples'],80)
        selected=c.select_threshold(self.project['validation_labels'],self.project['validation_scores'],5,1)
        self.assertEqual(selected['threshold'],self.project['artifact']['threshold'])

    def test_preprocessor_fits_train_rows_only(self):
        x,_=c.make_mixed_data()
        train=self.project['indices']['train']
        expected=np.nanmedian(x[train,:3].astype(float),axis=0)
        imputer=self.project['artifact']['model'][0].named_transformers_['numeric'][0]
        np.testing.assert_allclose(imputer.statistics_,expected)

    def test_reproducible_project(self):
        other=c.experiment()
        self.assertEqual(other['test'],self.project['test'])
        np.testing.assert_array_equal(other['validation_scores'],self.project['validation_scores'])

    def test_record_key_order_does_not_change_features(self):
        record=c.sample_records()[0]
        reverse=dict(reversed(list(record.items())))
        np.testing.assert_array_equal(c.records_to_array([record]),c.records_to_array([reverse]))

    def test_invalid_schema_rejected(self):
        record=c.sample_records()[0]
        del record['plan']
        with self.assertRaises(ValueError):
            c.records_to_array([record])

    def test_nonfinite_or_nonnumeric_rejected(self):
        for value in (float('inf'),'5',True):
            record=c.sample_records()[0];record['weekly_usage']=value
            with self.assertRaises(ValueError):
                c.records_to_array([record])

    def test_empty_prediction_rejected(self):
        with self.assertRaises(ValueError):
            c.records_to_array([])

    def test_missing_and_new_category_allowed(self):
        result=c.predict_records(self.project['artifact'],c.sample_records())
        self.assertEqual(len(result['scores']),3)
        self.assertTrue(all(0<=p<=1 for p in result['scores']))

    def test_actual_save_load_predictions(self):
        payload=self.project['artifact']
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'artifact.joblib'
            c.save_artifact(path,payload)
            loaded=c.load_artifact(path)
            self.assertEqual(c.predict_records(payload,c.sample_records()),c.predict_records(loaded,c.sample_records()))
            with self.assertRaises(FileExistsError):
                c.save_artifact(path,payload)

    def test_version_mismatch_rejected(self):
        payload=copy.copy(self.project['artifact']);payload['versions']={'sklearn':'old'}
        with self.assertRaises(ValueError):
            c.predict_records(payload,c.sample_records())

    def test_clone_does_not_retain_fitted_state(self):
        unfitted=clone(self.project['artifact']['model'])
        self.assertFalse(hasattr(unfitted[-1],'coef_'))

    def test_invalid_config(self):
        for config in (c.Config(samples=10),c.Config(folds=1),c.Config(false_negative_cost=-1)):
            with self.assertRaises(ValueError):
                config.validate()

    def test_all_30_entries_offline_from_other_cwd(self):
        previous=Path.cwd()
        def deny(*args,**kwargs):
            raise AssertionError('Default examples must be offline')
        with tempfile.TemporaryDirectory() as folder:
            try:
                os.chdir(folder)
                with patch.object(socket.socket,'connect',deny),patch.object(socket,'create_connection',deny):
                    for number in range(1,31):
                        with self.subTest(example=number),contextlib.redirect_stdout(io.StringIO()) as out:
                            result=entry(number).main([])
                            self.assertEqual(json.loads(out.getvalue()),result)
            finally:
                os.chdir(previous)


if __name__=='__main__':
    with threadpool_limits(limits=1):
        unittest.main()
