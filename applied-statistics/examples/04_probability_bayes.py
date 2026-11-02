"""Offline synthetic teaching experiment: 04_probability_bayes."""
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
    prior=.1;sensitivity=.8;false_positive=.2
    positive=prior*sensitivity+(1-prior)*false_positive
    result={'P_positive':positive,'P_condition_given_positive':prior*sensitivity/positive,'independent_example_P_A_and_B':.3*.4,'example':'abstract inspection classifier'}
    return emit(result)

if __name__=="__main__":
    main()
