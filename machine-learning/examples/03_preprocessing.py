"""Fit imputation and scaling only on training rows."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        train=np.array([[1.,2.],[3.,np.nan],[5.,6.]])
        validation=np.array([[100.,np.nan]])
        preprocess=make_pipeline(SimpleImputer(strategy='median',keep_empty_features=True),StandardScaler())
        transformed=preprocess.fit_transform(train)
        before=preprocess[0].statistics_.copy()
        heldout=preprocess.transform(validation)
        result={'imputation_statistics':before,'training_means':preprocess[1].mean_,
                'transformed_train_mean':transformed.mean(0),'transformed_validation':heldout,
                'statistics_unchanged':bool(np.array_equal(before,preprocess[0].statistics_))}
    return emit(result)

if __name__ == "__main__":
    main()
