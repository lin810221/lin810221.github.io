"""Permutation importance on held-out rows; associations are not causes."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        rng=np.random.default_rng(7)
        x=rng.normal(size=(200,3));y=4*x[:,0]+rng.normal(0,.1,200)
        a,b,c,d=train_test_split(x,y,test_size=.3,random_state=7)
        model=Ridge(alpha=1.).fit(a,c)
        importance=permutation_importance(model,b,d,n_repeats=5,random_state=7,scoring='neg_mean_absolute_error',n_jobs=1)
        result={'mean_score_drop':importance.importances_mean,'std_score_drop':importance.importances_std,
                'note':'importance is model/data/metric-specific; correlated features may share signal'}
    return emit(result)

if __name__ == "__main__":
    main()
