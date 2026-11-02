"""Offline synthetic teaching experiment: 14_variance_interval."""
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
    result=variance_ci([8,9,10,11,12,9,10,11,8,12]);result['sd_ci']=np.sqrt(result['ci'])
    return emit(result)

if __name__=="__main__":
    main()
