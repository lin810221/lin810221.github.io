"""Sigmoid calibration uses out-of-fold base-estimator scores."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from course_core import binary_data,holdout,probability,binary_metrics

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data()
        a,b,c,d=holdout(x,y)
        base=make_pipeline(StandardScaler(),LinearSVC(C=.5,random_state=7))
        model=CalibratedClassifierCV(base,method='sigmoid',cv=3).fit(a,c)
        result={'holdout':binary_metrics(d,probability(model,b)),
                'calibrated_members':len(model.calibrated_classifiers_),
                'note':'calibration quality must be evaluated; not guaranteed to improve every dataset'}
    return emit(result)

if __name__ == "__main__":
    main()
