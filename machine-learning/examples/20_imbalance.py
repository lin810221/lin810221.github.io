"""Class weights and thresholds address different decisions."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from course_core import holdout,probability,binary_metrics

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=make_classification(n_samples=400,n_features=6,n_informative=4,n_redundant=0,
                                weights=[.9,.1],random_state=7)
        a,b,c,d=holdout(x,y)
        model=make_pipeline(StandardScaler(),LogisticRegression(class_weight='balanced',l1_ratio=0,max_iter=1000)).fit(a,c)
        scores=probability(model,b)
        result={'test_prevalence':float(d.mean()),'threshold_0_5':binary_metrics(d,scores,.5),
                'fixed_lower_threshold':binary_metrics(d,scores,.25),
                'note':'these settings are demonstrations; tune decisions on validation, not this holdout'}
    return emit(result)

if __name__ == "__main__":
    main()
