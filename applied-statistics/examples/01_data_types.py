"""Offline synthetic teaching experiment: 01_data_types."""
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
    labels=['A','B','A','C','B','A']
    counts_=pd.Series(labels).value_counts().sort_index()
    result={'counts':counts_.to_dict(),'relative_frequency':(counts_/len(labels)).to_dict(),'n':len(labels)}
    return emit(result)

if __name__=="__main__":
    main()
