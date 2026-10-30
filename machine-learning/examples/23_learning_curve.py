"""Learning curves are computed on training folds with preprocessing inside."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.model_selection import learning_curve,StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from course_core import binary_data,split_indices

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data()
        train=split_indices(y)['train']
        model=make_pipeline(StandardScaler(),LogisticRegression(l1_ratio=0,max_iter=1000))
        sizes,train_scores,val_scores=learning_curve(model,x[train],y[train],train_sizes=[.5,.75,1.],
            cv=StratifiedKFold(3,shuffle=True,random_state=7),scoring='average_precision',shuffle=True,random_state=7,n_jobs=1)
        result={'training_rows_per_fold':sizes,'train_ap':train_scores.mean(1),'validation_ap':val_scores.mean(1),
                'note':'diagnostic curve, not proof of a single cause or a final test result'}
    return emit(result)

if __name__ == "__main__":
    main()
