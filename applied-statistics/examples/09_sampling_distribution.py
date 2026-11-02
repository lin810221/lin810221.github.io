"""Offline synthetic teaching experiment: 09_sampling_distribution."""
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
    rng=np.random.default_rng(SEED);n=30;means=rng.exponential(scale=1,size=(4000,n)).mean(axis=1)
    result={'population_mean':1,'population_sd':1,'n':n,'replicates':len(means),'simulated_mean_of_means':means.mean(),'simulated_se':means.std(ddof=1),'theoretical_se':1/np.sqrt(n),'note':'illustration for an exponential population, not a universal n=30 rule'}
    return emit(result)

if __name__=="__main__":
    main()
