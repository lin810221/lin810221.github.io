"""MAE, RMSE and negative R2 for a poor predictor."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from course_core import regression_metrics

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        y=np.array([1.,2.,3.])
        prediction=np.array([1.,2.,5.])
        result={'worked_example':regression_metrics(y,prediction),
                'poor_constant':regression_metrics(y,np.full(3,10.)),
                'note':'RMSE uses target units; R2 may be negative'}
    return emit(result)

if __name__ == "__main__":
    main()
