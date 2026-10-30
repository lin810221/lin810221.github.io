"""Stratified, grouped and time-respecting splits."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.model_selection import GroupKFold, TimeSeriesSplit
from course_core import binary_data, split_indices

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data()
        parts=split_indices(y)
        groups=np.repeat(np.arange(12),3)
        group_folds=[]
        for train,test in GroupKFold(3).split(np.zeros((36,1)),groups=groups):
            group_folds.append({'train_groups':np.unique(groups[train]),'test_groups':np.unique(groups[test]),
                                'overlap':len(set(groups[train])&set(groups[test]))})
        time_folds=[{'last_train':int(a[-1]),'first_test':int(b[0])}
                    for a,b in TimeSeriesSplit(3,gap=1).split(np.arange(20))]
        result={'sizes':{k:len(v) for k,v in parts.items()},
                'positive_rates':{k:float(y[v].mean()) for k,v in parts.items()},
                'group_folds':group_folds,'time_folds':time_folds}
    return emit(result)

if __name__ == "__main__":
    main()
