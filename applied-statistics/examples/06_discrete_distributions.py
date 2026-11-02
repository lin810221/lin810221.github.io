"""Offline synthetic teaching experiment: 06_discrete_distributions."""
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
    result={'uniform_mean':stats.randint.mean(1,7),'binomial_P_X_eq_3':stats.binom.pmf(3,10,.2),'hypergeometric_P_X_eq_2':stats.hypergeom.pmf(2,20,5,4),'poisson_P_X_ge_3':stats.poisson.sf(2,2),'poisson_mean_variance':[stats.poisson.mean(2),stats.poisson.var(2)]}
    return emit(result)

if __name__=="__main__":
    main()
