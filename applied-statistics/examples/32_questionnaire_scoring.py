"""Offline synthetic teaching experiment: 32_questionnaire_scoring."""
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
    data=load_survey()
    result={'rows':len(data),'missing_by_item':data[['q1','q2','q3_negative','q4','q5','q6']].isna().sum().to_dict(),'service_valid_n':int(data.service.notna().sum()),'first_reverse_pair':[data.q3_negative.iloc[0],data.q3.iloc[0]],'score_policy':'mean of q1,q2,q3 with >=2 responses'}
    return emit(result)

if __name__=="__main__":
    main()
