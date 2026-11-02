"""Offline synthetic teaching experiment: 11_mean_intervals."""
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
    x=[48,51,49,52,50,47,53,50,49,51]
    result={'unknown_sigma_t':mean_ci(x),'known_sigma_z':mean_ci(x,sigma=3),'same_data_different_assumptions':True}
    return emit(result)

if __name__=="__main__":
    main()
