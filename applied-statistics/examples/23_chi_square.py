"""Offline synthetic teaching experiment: 23_chi_square."""
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
    table=[[30,20],[20,30],[25,25]]
    result=contingency(table)
    result['fisher_sparse_2x2_p']=stats.fisher_exact([[1,4],[6,1]]).pvalue
    return emit(result)

if __name__=="__main__":
    main()
