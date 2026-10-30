"""Compare candidates using identical training CV folds, not final test."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold,cross_val_score
from course_core import binary_data,split_indices

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data()
        train=split_indices(y)['train']
        folds=list(StratifiedKFold(3,shuffle=True,random_state=7).split(x[train],y[train]))
        models={'dummy':DummyClassifier(strategy='prior'),
                'logistic':make_pipeline(StandardScaler(),LogisticRegression(l1_ratio=0,max_iter=1000)),
                'forest':RandomForestClassifier(n_estimators=30,max_depth=4,random_state=7,n_jobs=1)}
        reports={name:cross_val_score(model,x[train],y[train],cv=folds,scoring='average_precision',n_jobs=1)
                 for name,model in models.items()}
        result={'training_cv_average_precision':reports,'test_used':False,
                'note':'same folds; repeated selection still requires final evaluation'}
    return emit(result)

if __name__ == "__main__":
    main()
