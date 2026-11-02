"""Offline synthetic teaching experiment: 39_survey_anova_posthoc."""
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
    data=load_survey();groups=[data.loc[data.group==g,'service'].dropna().to_numpy() for g in ['A','B','C']]
    result={'group_order':['A','B','C'],'welch_anova':one_way(groups,equal_var=False),'games_howell':posthoc(groups,use_var='unequal')}
    return emit(result)

if __name__=="__main__":
    main()
