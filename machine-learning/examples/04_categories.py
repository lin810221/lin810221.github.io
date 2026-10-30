"""Unknown categories use the already fitted vocabulary."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.preprocessing import OneHotEncoder

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        encoder=OneHotEncoder(handle_unknown='ignore',sparse_output=False)
        encoder.fit(np.array([['basic'],['team'],['basic']]))
        result={'categories':encoder.categories_[0],
                'feature_names':encoder.get_feature_names_out(),
                'known_and_unknown':encoder.transform([['team'],['new_plan']]),
                'note':'unknown is all zeros, not a newly fitted feature'}
    return emit(result)

if __name__ == "__main__":
    main()
