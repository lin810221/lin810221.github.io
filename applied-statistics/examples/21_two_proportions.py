"""Offline synthetic teaching experiment: 21_two_proportions."""
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
    from statsmodels.stats.proportion import proportions_ztest,confint_proportions_2indep
    z,p=proportions_ztest([45,30],[100,100],alternative='two-sided')
    ci=confint_proportions_2indep(45,100,30,100,method='newcomb',compare='diff')
    result={'difference_A_minus_B':.15,'pooled_null_z':z,'p':p,'newcombe_difference_ci':ci,'note':'independent groups; interval uses a different approximation than the pooled z test'}
    return emit(result)

if __name__=="__main__":
    main()
