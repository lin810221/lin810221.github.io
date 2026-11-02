"""Offline synthetic teaching experiment: 08_sampling_designs."""
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
    rng=np.random.default_rng(SEED);population=np.arange(100)
    srs=rng.choice(population,10,replace=False)
    stratified=np.concatenate([rng.choice(np.arange(0,60),6,replace=False),rng.choice(np.arange(60,100),4,replace=False)])
    clusters=rng.choice(10,2,replace=False);cluster_sample=np.concatenate([np.arange(c*10,(c+1)*10) for c in clusters])
    start=int(rng.integers(0,10));systematic=np.arange(start,100,10)
    result={'srs':srs,'proportionate_stratified':stratified,'selected_clusters':clusters,'all_members_in_selected_clusters':cluster_sample,'systematic_random_start':start,'systematic':systematic}
    return emit(result)

if __name__=="__main__":
    main()
