"""Offline synthetic teaching experiment: 31_diagnostics."""
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
    x,y=regression_data();model=sm.OLS(y,sm.add_constant(x)).fit();from statsmodels.stats.diagnostic import het_breuschpagan
    lm,lmp,f,fp=het_breuschpagan(model.resid,model.model.exog)
    result={'breusch_pagan_lm':lm,'lm_p':lmp,'classical_and_HC3':regression(),'note':'small-sample diagnostics do not certify assumptions; HC3 does not fix dependent observations or nonlinear misspecification'}
    return emit(result)

if __name__=="__main__":
    main()
