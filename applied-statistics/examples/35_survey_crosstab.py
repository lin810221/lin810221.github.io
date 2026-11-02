"""Offline synthetic teaching experiment: 35_survey_crosstab."""
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
    data=load_survey();table=pd.crosstab(data.group,data.category)
    result={'row_labels':list(table.index),'column_labels':list(table.columns),'counts':table.to_numpy(),'row_percent':table.div(table.sum(axis=1),axis=0).to_numpy(),'pearson_test':contingency(table.to_numpy())}
    return emit(result)

if __name__=="__main__":
    main()
