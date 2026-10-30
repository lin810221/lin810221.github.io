"""Inspect a bounded decision tree and its actual first split."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.tree import DecisionTreeClassifier
from course_core import binary_data,holdout,probability,binary_metrics

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data()
        a,b,c,d=holdout(x,y)
        model=DecisionTreeClassifier(max_depth=3,min_samples_leaf=5,random_state=7).fit(a,c)
        result={'depth':model.get_depth(),'leaves':model.get_n_leaves(),
                'first_split_feature':model.tree_.feature[0],'first_split_threshold':model.tree_.threshold[0],
                'holdout':binary_metrics(d,probability(model,b))}
    return emit(result)

if __name__ == "__main__":
    main()
