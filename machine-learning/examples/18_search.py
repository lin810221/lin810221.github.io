"""GridSearchCV searches pipeline parameters using training folds only."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.model_selection import GridSearchCV,StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from course_core import binary_data,split_indices

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data()
        train=split_indices(y)['train']
        pipeline=make_pipeline(StandardScaler(),LogisticRegression(l1_ratio=0,max_iter=1000))
        search=GridSearchCV(pipeline,{'logisticregression__C':[.01,.1,1.,10.]},
            cv=StratifiedKFold(3,shuffle=True,random_state=7),scoring='average_precision',n_jobs=1).fit(x[train],y[train])
        result={'best_parameters':search.best_params_,'best_training_cv_score':search.best_score_,
                'candidates':len(search.cv_results_['params']),'test_used':False}
    return emit(result)

if __name__ == "__main__":
    main()
