"""Offline synthetic teaching experiment: 10_sampling_pivots."""
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
    result={'t_975_df9':stats.t.ppf(.975,9),'chi2_025_df9':stats.chi2.ppf(.025,9),'F_95_df4_10':stats.f.ppf(.95,4,10),'t_two_sided_tail_at_2':2*stats.t.sf(2,9),'inverse_check':stats.t.cdf(stats.t.ppf(.975,9),9)}
    return emit(result)

if __name__=="__main__":
    main()
