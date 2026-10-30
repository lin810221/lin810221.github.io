"""Scaled RBF SVM uses decision scores, not fake probabilities."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score,roc_auc_score
from course_core import binary_data,holdout

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data()
        a,b,c,d=holdout(x,y)
        model=make_pipeline(StandardScaler(),SVC(C=1.,gamma='scale',kernel='rbf')).fit(a,c)
        result={'accuracy':accuracy_score(d,model.predict(b)),
                'roc_auc_from_decision_scores':roc_auc_score(d,model.decision_function(b)),
                'support_vectors':model[-1].n_support_,
                'note':'decision_function values are not calibrated probabilities'}
    return emit(result)

if __name__ == "__main__":
    main()
