"""Histogram gradient boosting; bounded rounds, no external boosting package."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.ensemble import HistGradientBoostingClassifier
from course_core import binary_data,holdout,probability,binary_metrics

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data()
        a,b,c,d=holdout(x,y)
        a=a.copy();a[::13,0]=np.nan
        model=HistGradientBoostingClassifier(max_iter=50,learning_rate=.1,max_leaf_nodes=7,
                                            early_stopping=False,random_state=7).fit(a,c)
        result={'rounds':model.n_iter_,'training_missing_rows':int(np.isnan(a).any(1).sum()),
                'holdout':binary_metrics(d,probability(model,b))}
    return emit(result)

if __name__ == "__main__":
    main()
