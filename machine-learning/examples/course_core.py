"""Offline, synthetic scikit-learn teaching tools. Course baseline: 1.9.1."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import platform
import joblib
import numpy as np
import scipy
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.datasets import make_classification, make_regression
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, average_precision_score, brier_score_loss,
    confusion_matrix, f1_score, log_loss, mean_absolute_error, precision_score,
    r2_score, recall_score, roc_auc_score, root_mean_squared_error)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from threadpoolctl import threadpool_limits

SEED = 7
SCHEMA = ('tenure_months', 'weekly_usage', 'support_tickets', 'plan')


def emit(report):
    def convert(value):
        if isinstance(value, np.ndarray):
            return value.tolist()
        if isinstance(value, np.generic):
            return value.item()
        raise TypeError(type(value).__name__)
    plain = json.loads(json.dumps(report, default=convert, allow_nan=False))
    print(json.dumps(plain, ensure_ascii=True, indent=2, allow_nan=False))
    return plain


def binary_data(n=300, seed=SEED):
    return make_classification(n_samples=n, n_features=6, n_informative=4,
        n_redundant=0, weights=[.75,.25], class_sep=1.1, random_state=seed)


def regression_data(n=200, seed=SEED):
    return make_regression(n_samples=n, n_features=5, n_informative=3,
        noise=8., random_state=seed)


def holdout(x, y):
    return train_test_split(x, y, test_size=.25, random_state=SEED,
                            stratify=y if np.issubdtype(np.asarray(y).dtype, np.integer) else None)


def split_indices(y, seed=SEED):
    y = np.asarray(y)
    if y.ndim != 1 or len(y)<30 or set(np.unique(y)) != {0,1}:
        raise ValueError('Need at least 30 binary-labelled rows')
    train, rest = train_test_split(np.arange(len(y)), test_size=.4, stratify=y, random_state=seed)
    validation, test = train_test_split(rest, test_size=.5, stratify=y[rest], random_state=seed+1)
    return {'train':train, 'validation':validation, 'test':test}


def probability(model, x, positive=1):
    classes = np.asarray(model.classes_)
    found = np.flatnonzero(classes == positive)
    if len(found)!=1:
        raise ValueError('Positive class missing or ambiguous')
    return model.predict_proba(x)[:,int(found[0])]


def binary_metrics(y, scores, threshold=.5):
    y, scores = np.asarray(y), np.asarray(scores, dtype=float)
    if y.ndim!=1 or scores.shape!=y.shape or len(y)==0 or not np.isin(y,[0,1]).all():
        raise ValueError('Expected equal, nonempty binary labels and scores')
    if not np.isfinite(scores).all() or np.any((scores<0)|(scores>1)) or not np.isfinite(threshold):
        raise ValueError('Expected finite probability scores and threshold')
    pred = (scores>=threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y,pred,labels=[0,1]).ravel()
    return {'samples':len(y), 'tp':int(tp), 'fp':int(fp), 'fn':int(fn), 'tn':int(tn),
      'accuracy':float(accuracy_score(y,pred)), 'precision':float(precision_score(y,pred,zero_division=0)),
      'recall':float(recall_score(y,pred,zero_division=0)), 'f1':float(f1_score(y,pred,zero_division=0)),
      'average_precision':float(average_precision_score(y,scores)) if np.any(y==1) else None,
      'roc_auc':float(roc_auc_score(y,scores)) if len(np.unique(y))==2 else None,
      'brier':float(brier_score_loss(y,scores)),
      'log_loss':float(log_loss(y,np.column_stack([1-scores,scores]),labels=[0,1]))}


def regression_metrics(y, prediction):
    y, prediction = np.asarray(y,dtype=float), np.asarray(prediction,dtype=float)
    if y.ndim!=1 or y.shape!=prediction.shape or len(y)<2 or not np.isfinite(y).all() or not np.isfinite(prediction).all():
        raise ValueError('Expected finite, matching regression vectors with at least two rows')
    return {'mae':float(mean_absolute_error(y,prediction)),
            'rmse':float(root_mean_squared_error(y,prediction)),
            'r2':float(r2_score(y,prediction))}


def select_threshold(y, scores, false_negative_cost=5., false_positive_cost=1.):
    # Selection must use validation / out-of-fold scores, never the final test.
    if any(not np.isfinite(v) or v<0 for v in (false_negative_cost,false_positive_cost)):
        raise ValueError('Finite, nonnegative costs required')
    binary_metrics(y,scores)
    candidates = np.unique(np.r_[0.,scores,np.nextafter(1.,2.)])
    rows=[]
    for threshold in candidates:
        metrics=binary_metrics(y,scores,float(threshold))
        cost=metrics['fn']*false_negative_cost+metrics['fp']*false_positive_cost
        rows.append((float(cost),float(threshold)))
    # Deterministic tie-break: prefer the lower threshold (higher coverage).
    cost,threshold=min(rows)
    return {'threshold':threshold,'validation_cost':cost,'candidates':len(candidates)}


def make_mixed_data(n=400, seed=SEED):
    rng=np.random.default_rng(seed)
    tenure=rng.integers(1,61,size=n).astype(float)
    usage=rng.normal(5,2,size=n).clip(0,12)
    tickets=rng.poisson(1.5,size=n).astype(float)
    plan=rng.choice(['basic','plus','team'],size=n,p=[.5,.3,.2])
    risk=1.5-.8*usage+.65*tickets-.012*tenure+.8*(plan=='basic')
    score=1/(1+np.exp(-risk))
    y=(rng.random(n)<score).astype(int)
    x=np.empty((n,4),dtype=object)
    x[:,0],x[:,1],x[:,2],x[:,3]=tenure,usage,tickets,plan
    for j in range(3):
        x[rng.random(n)<.06,j]=np.nan
    x[rng.random(n)<.04,3]=np.nan
    return x,y


def mixed_pipeline(C=1.):
    numeric=Pipeline([('impute',SimpleImputer(strategy='median',add_indicator=True,keep_empty_features=True)),
                      ('scale',StandardScaler())])
    category=Pipeline([('impute',SimpleImputer(strategy='constant',fill_value='MISSING',keep_empty_features=True)),
                       ('encode',OneHotEncoder(handle_unknown='ignore',sparse_output=False))])
    preprocess=ColumnTransformer([('numeric',numeric,[0,1,2]),('category',category,[3])],remainder='drop')
    return Pipeline([('preprocess',preprocess),('model',LogisticRegression(C=C,l1_ratio=0,max_iter=1000))])


@dataclass(frozen=True)
class Config:
    seed:int=SEED
    samples:int=400
    folds:int=3
    false_negative_cost:float=5.
    false_positive_cost:float=1.

    def validate(self):
        if not isinstance(self.samples,int) or self.samples<100 or not isinstance(self.folds,int) or self.folds<2:
            raise ValueError('At least 100 samples and two folds required')
        if any(not np.isfinite(v) or v<0 for v in (self.false_negative_cost,self.false_positive_cost)):
            raise ValueError('Invalid costs')


def experiment(config=Config()):
    config.validate()
    x,y=make_mixed_data(config.samples,config.seed)
    indices=split_indices(y,config.seed)
    train,validation,test=(indices[k] for k in ('train','validation','test'))
    cv=StratifiedKFold(config.folds,shuffle=True,random_state=config.seed)
    search=GridSearchCV(mixed_pipeline(),{'model__C':[.1,1.,10.]},cv=cv,
                        scoring='average_precision',n_jobs=1,error_score='raise')
    with threadpool_limits(limits=1):
        search.fit(x[train],y[train])
        validation_scores=probability(search.best_estimator_,x[validation])
        selection=select_threshold(y[validation],validation_scores,
                                    config.false_negative_cost,config.false_positive_cost)
        # Model and threshold are fixed before this one final test evaluation.
        test_metrics=binary_metrics(y[test],probability(search.best_estimator_,x[test]),selection['threshold'])
    payload={'format_version':1,'schema':list(SCHEMA),'model':search.best_estimator_,
       'threshold':selection['threshold'],'positive_class':1,'config':asdict(config),
       'versions':{'sklearn':sklearn.__version__,'numpy':np.__version__,
                   'scipy':scipy.__version__,'python':platform.python_version()},
       'data':'synthetic mixed features; no real customer data',
       'selection':{'best_parameters':search.best_params_,'training_cv_ap':float(search.best_score_),**selection}}
    return {'artifact':payload,'indices':indices,'validation_scores':validation_scores,
            'validation_labels':y[validation],'test':test_metrics,
            'split_sizes':{k:len(v) for k,v in indices.items()}}


def records_to_array(records):
    if not isinstance(records,list) or not records:
        raise ValueError('Provide a nonempty list of records')
    rows=[]
    for record in records:
        if not isinstance(record,dict) or set(record)!=set(SCHEMA):
            raise ValueError('Record keys must exactly match the saved feature schema')
        values=[]
        for key in SCHEMA[:3]:
            value=record[key]
            if value is None:
                values.append(np.nan)
            elif isinstance(value,(int,float)) and not isinstance(value,bool) and np.isfinite(value):
                values.append(float(value))
            else:
                raise ValueError('Numeric values must be finite numbers or null')
        category=record[SCHEMA[3]]
        if category is not None and (not isinstance(category,str) or not category.strip()):
            raise ValueError('Plan must be a nonempty string or null')
        values.append(np.nan if category is None else category)
        rows.append(values)
    return np.array(rows,dtype=object)


def predict_records(payload,records):
    if payload.get('format_version')!=1 or payload.get('schema')!=list(SCHEMA):
        raise ValueError('Artifact schema mismatch')
    if payload['versions']['sklearn']!=sklearn.__version__:
        raise ValueError('Use the same scikit-learn version as training')
    scores=probability(payload['model'],records_to_array(records),payload['positive_class'])
    return {'scores':scores.tolist(),'labels':(scores>=payload['threshold']).astype(int).tolist(),
            'threshold':payload['threshold']}


def save_artifact(path,payload):
    path=Path(path)
    if path.exists():
        raise FileExistsError('Choose a new artifact filename')
    path.parent.mkdir(parents=True,exist_ok=True)
    joblib.dump(payload,path,compress=3)


def load_artifact(path):
    # Trusted local artifact only. Joblib unpickling can execute code.
    payload=joblib.load(path)
    if not isinstance(payload,dict) or payload.get('format_version')!=1:
        raise ValueError('Unknown artifact format')
    if payload['versions']['sklearn']!=sklearn.__version__:
        raise ValueError('Unsupported scikit-learn version')
    return payload


def sample_records():
    return json.loads((Path(__file__).parent/'data/prediction_records.json').read_text(encoding='utf-8'))
