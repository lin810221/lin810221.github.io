"""Recover a known linear rule; not a generalization benchmark."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.linear_model import LinearRegression
from course_core import regression_metrics

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x=np.arange(-5.,6.).reshape(-1,1)
        y=3*x[:,0]+.5
        model=LinearRegression().fit(x,y)
        result={'coefficient':model.coef_,'intercept':model.intercept_,
                'training_sanity_check':regression_metrics(y,model.predict(x)),
                'new_x_prediction':model.predict([[6.]])}
    return emit(result)

if __name__ == "__main__":
    main()
