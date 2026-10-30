"""Real TunedThresholdClassifierCV tunes only within training data."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.model_selection import TunedThresholdClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import balanced_accuracy_score
from course_core import binary_data,holdout

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data()
        a,b,c,d=holdout(x,y)
        base=make_pipeline(StandardScaler(),LogisticRegression(l1_ratio=0,max_iter=1000))
        model=TunedThresholdClassifierCV(base,scoring='balanced_accuracy',cv=3,thresholds=30).fit(a,c)
        result={'selected_threshold':model.best_threshold_,'training_cv_balanced_accuracy':model.best_score_,
                'holdout_balanced_accuracy':balanced_accuracy_score(d,model.predict(b)),
                'note':'holdout was not used for threshold selection'}
    return emit(result)

if __name__ == "__main__":
    main()
