"""Offline synthetic teaching experiment: 26_posthoc."""
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
    groups=[[3,4,5,4],[5,6,7,6],[7,8,9,8]]
    result={'tukey':posthoc(groups),'games_howell':posthoc(groups,use_var='unequal'),'holm_example':multipletests([.01,.03,.2],method='holm')[1]}
    return emit(result)

if __name__=="__main__":
    main()
