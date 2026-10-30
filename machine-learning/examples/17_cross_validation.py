"""Leakage-safe preprocessing is fitted inside each fold."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.model_selection import StratifiedKFold,cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from course_core import binary_data

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data()
        model=make_pipeline(StandardScaler(),LogisticRegression(l1_ratio=0,max_iter=1000))
        report=cross_validate(model,x,y,cv=StratifiedKFold(3,shuffle=True,random_state=7),
            scoring={'ap':'average_precision','accuracy':'accuracy'},return_estimator=True,n_jobs=1)
        result={'fold_ap':report['test_ap'],'fold_accuracy':report['test_accuracy'],
                'fold_specific_scaler_means':[m[0].mean_ for m in report['estimator']],
                'note':'fold test scores mean validation folds, not a separately reserved final test'}
    return emit(result)

if __name__ == "__main__":
    main()
