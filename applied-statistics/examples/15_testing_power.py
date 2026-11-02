"""Offline synthetic teaching experiment: 15_testing_power."""
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
    result={'p_two_sided_z_2':2*stats.norm.sf(2),'null_rejection_probability':z_power(30,0),'power_delta_half':z_power(30,.5),'power_n_100':z_power(100,.5),'assumptions':'two-sided z test, known sigma=1, independent normal observations'}
    return emit(result)

if __name__=="__main__":
    main()
