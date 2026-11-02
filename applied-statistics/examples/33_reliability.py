"""Offline synthetic teaching experiment: 33_reliability."""
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
    data=load_survey();correct=data[['q1','q2','q3']].dropna();wrong=data.loc[correct.index,['q1','q2','q3_negative']]
    result={'n_complete':len(correct),'alpha_after_reverse_scoring':alpha_reliability(correct),'alpha_without_reverse_scoring':alpha_reliability(wrong),'limit':'alpha alone does not establish validity or unidimensionality'}
    return emit(result)

if __name__=="__main__":
    main()
