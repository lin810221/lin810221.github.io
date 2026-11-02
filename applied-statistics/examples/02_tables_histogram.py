"""Offline synthetic teaching experiment: 02_tables_histogram."""
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
    x=np.array([1.,2.,2.,3.,4.,6.,8.,9.]);edges=np.array([0.,3.,6.,9.])
    frequency,bins=np.histogram(x,bins=edges)
    result={'edges':bins,'counts':frequency,'relative_frequency':frequency/len(x),'density':frequency/(len(x)*np.diff(bins)),'closure':'left-closed, right-open except last bin includes right endpoint'}
    return emit(result)

if __name__=="__main__":
    main()
