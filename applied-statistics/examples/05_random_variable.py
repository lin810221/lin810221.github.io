"""Offline synthetic teaching experiment: 05_random_variable."""
import math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from course_core import (SEED,emit,describe,mean_ci,proportion_ci,variance_ci,
    sample_size_mean,one_t,welch,paired,z_power,variance_test,variance_ratio,
    contingency,one_way,posthoc,factorial,regression,regression_data,
    load_survey,alpha_reliability,factor_report,survey_report,save_report)

def main(argv=None):
    del argv
    values=np.array([0.,1.,2.]);p=np.array([.2,.5,.3]);mean=float(values@p)
    result={'expectation':mean,'variance':float(((values-mean)**2)@p),'cdf_at_1':float(p[:2].sum()),'uniform_continuous_interval_probability':stats.uniform.cdf(.7)-stats.uniform.cdf(.2)}
    return emit(result)

if __name__=="__main__":
    main()
