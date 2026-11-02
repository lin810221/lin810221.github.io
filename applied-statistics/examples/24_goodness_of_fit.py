"""Offline synthetic teaching experiment: 24_goodness_of_fit."""
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
    observed=np.array([18,22,20,16,24,20]);expected=np.full(6,20.)
    test=stats.chisquare(observed,f_exp=expected)
    result={'observed':observed,'expected':expected,'chi2':test.statistic,'df':5,'p':test.pvalue,'estimated_distribution_parameters':0}
    return emit(result)

if __name__=="__main__":
    main()
