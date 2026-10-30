"""IsolationForest uses a separate synthetic query set."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.ensemble import IsolationForest

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        rng=np.random.default_rng(7)
        normal=rng.normal(0,.4,(120,2))
        query=np.array([[0.,0.],[8.,8.]])
        model=IsolationForest(n_estimators=50,contamination=.05,random_state=7,n_jobs=1).fit(normal)
        result={'queries':query,'predictions':model.predict(query),'decision_function':model.decision_function(query),
                'note':'+1=inlier, -1=outlier; contamination controls the decision threshold'}
    return emit(result)

if __name__ == "__main__":
    main()
