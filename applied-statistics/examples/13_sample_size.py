"""Offline synthetic teaching experiment: 13_sample_size."""
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
    z=stats.norm.ppf(.975);margin=.05;p=.5
    result={'mean_sigma_10_margin_2':sample_size_mean(10,2),'proportion_worst_case_margin_05':math.ceil(z*z*p*(1-p)/margin**2),'planning':'normal approximation; independent sampling; no nonresponse or design-effect adjustment'}
    return emit(result)

if __name__=="__main__":
    main()
