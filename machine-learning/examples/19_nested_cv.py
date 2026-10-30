"""Outer folds evaluate the full inner hyperparameter search procedure."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.model_selection import GridSearchCV,StratifiedKFold,cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from course_core import binary_data

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data(n=180)
        pipeline=make_pipeline(StandardScaler(),LogisticRegression(l1_ratio=0,max_iter=1000))
        search=GridSearchCV(pipeline,{'logisticregression__C':[.1,1.]},
            cv=StratifiedKFold(3,shuffle=True,random_state=11),scoring='average_precision',n_jobs=1)
        outer=cross_val_score(search,x,y,cv=StratifiedKFold(3,shuffle=True,random_state=13),
                               scoring='average_precision',n_jobs=1)
        result={'outer_ap':outer,'mean_outer_ap':outer.mean(),'fits_roughly':3*(2*3+1),
                'note':'outer scores evaluate selection; not the optimistic best inner score'}
    return emit(result)

if __name__ == "__main__":
    main()
