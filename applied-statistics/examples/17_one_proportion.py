"""Offline synthetic teaching experiment: 17_one_proportion."""
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
    test=stats.binomtest(8,10,p=.5,alternative='two-sided')
    result={'successes':8,'n':10,'null':.5,'exact_p':test.pvalue,'wilson_interval':proportion_ci(8,10),'note':'exact test and Wilson interval are not an inversion pair'}
    return emit(result)

if __name__=="__main__":
    main()
