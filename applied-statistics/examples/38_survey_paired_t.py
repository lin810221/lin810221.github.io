"""Offline synthetic teaching experiment: 38_survey_paired_t."""
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
    data=load_survey();before=data[['id','before']].sample(frac=1,random_state=7);after=data[['id','after']].sample(frac=1,random_state=11)
    matched=before.merge(after,on='id',validate='one_to_one');result=paired(matched.before,matched.after);result['matched_by']='unique respondent id, not row position'
    return emit(result)

if __name__=="__main__":
    main()
