"""Current LogisticRegression API with raw classes and probabilities."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from course_core import binary_data,holdout,probability,binary_metrics

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data()
        a,b,c,d=holdout(x,y)
        model=make_pipeline(StandardScaler(),LogisticRegression(C=1.,l1_ratio=0,max_iter=1000)).fit(a,c)
        scores=probability(model,b)
        result={'classes':model.classes_,'first_five_probabilities':scores[:5],
                'probability_row_sums':model.predict_proba(b)[:5].sum(1),
                'holdout':binary_metrics(d,scores)}
    return emit(result)

if __name__ == "__main__":
    main()
