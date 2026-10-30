"""Bagged randomized trees on a fixed synthetic holdout."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.ensemble import RandomForestClassifier
from course_core import binary_data,holdout,probability,binary_metrics

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data()
        a,b,c,d=holdout(x,y)
        model=RandomForestClassifier(n_estimators=60,min_samples_leaf=3,max_features='sqrt',
                                     random_state=7,n_jobs=1).fit(a,c)
        result={'trees':len(model.estimators_),'holdout':binary_metrics(d,probability(model,b)),
                'impurity_importance':model.feature_importances_,
                'note':'impurity importance is not causal importance'}
    return emit(result)

if __name__ == "__main__":
    main()
