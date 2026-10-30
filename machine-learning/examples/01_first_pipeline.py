"""A complete fixed-model classification workflow; synthetic data."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from course_core import binary_data, holdout, probability, binary_metrics

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data()
        x_train,x_test,y_train,y_test=holdout(x,y)
        model=make_pipeline(StandardScaler(),LogisticRegression(l1_ratio=0,max_iter=1000))
        model.fit(x_train,y_train)
        baseline=DummyClassifier(strategy='prior').fit(x_train,y_train)
        result={'pipeline':binary_metrics(y_test,probability(model,x_test)),
                'dummy':binary_metrics(y_test,probability(baseline,x_test)),
                'scope':'fixed settings, synthetic holdout; no production accuracy claim'}
    return emit(result)

if __name__ == "__main__":
    main()
