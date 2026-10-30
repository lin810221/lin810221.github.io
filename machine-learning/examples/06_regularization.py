"""Compare ridge and lasso on the same fixed split."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.linear_model import Ridge,Lasso
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from course_core import regression_data, holdout, regression_metrics

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=regression_data()
        a,b,c,d=holdout(x,y)
        reports={}
        for name,estimator in [('ridge',Ridge(alpha=10.)),('lasso',Lasso(alpha=1.,max_iter=5000))]:
            model=make_pipeline(StandardScaler(),estimator).fit(a,c)
            reports[name]={'coefficients_in_scaled_units':model[-1].coef_,
                           'holdout':regression_metrics(d,model.predict(b))}
        result={'fixed_settings_demonstration':reports,'selection':'do not choose hyperparameters on these holdout scores'}
    return emit(result)

if __name__ == "__main__":
    main()
