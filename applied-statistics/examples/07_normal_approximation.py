"""Offline synthetic teaching experiment: 07_normal_approximation."""
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
    n=100;p=.4;lower=35;upper=45;sd=np.sqrt(n*p*(1-p))
    exact=stats.binom.cdf(upper,n,p)-stats.binom.cdf(lower-1,n,p)
    approx=stats.norm.cdf((upper+.5-n*p)/sd)-stats.norm.cdf((lower-.5-n*p)/sd)
    result={'exact_binomial':exact,'normal_with_continuity_correction':approx,'absolute_error':abs(exact-approx),'np_nq':[n*p,n*(1-p)]}
    return emit(result)

if __name__=="__main__":
    main()
