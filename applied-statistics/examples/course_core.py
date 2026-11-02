"""Original, offline applied statistics examples. Synthetic data, not field evidence."""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd
import scipy
from scipy import stats
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multitest import multipletests
from statsmodels.multivariate.factor import Factor

SEED=20261102

def emit(report):
    def convert(x):
        if isinstance(x,np.ndarray):return x.tolist()
        if isinstance(x,np.generic):return x.item()
        raise TypeError(type(x).__name__)
    plain=json.loads(json.dumps(report,default=convert,allow_nan=False))
    print(json.dumps(plain,indent=2,ensure_ascii=True,allow_nan=False));return plain

def sample(values,minimum=2):
    x=np.asarray(values,dtype=float)
    if x.ndim!=1 or len(x)<minimum or not np.isfinite(x).all():raise ValueError('Finite one-dimensional sample required; missing values need an explicit policy')
    return x

def level_check(level):
    if not 0<level<1:raise ValueError('Confidence level must be between zero and one')

def counts(k,n):
    if any(isinstance(v,(bool,np.bool_)) or not isinstance(v,(int,np.integer)) for v in [k,n]) or n<1 or not 0<=k<=n:raise ValueError('Integer counts 0 <= k <= n required')

def describe(values,ratio_scale=False):
    x=sample(values);q=np.quantile(x,[.25,.5,.75],method='linear');mean=x.mean();sd=x.std(ddof=1)
    return {'n':len(x),'mean':mean,'median':q[1],'q1':q[0],'q3':q[2],'iqr':q[2]-q[0],'quartile_deviation':(q[2]-q[0])/2,
        'range':np.ptp(x),'mean_absolute_deviation_about_mean':np.abs(x-mean).mean(),'sample_variance':x.var(ddof=1),
        'sample_sd':sd,'cv':sd/mean if ratio_scale and mean>0 else None,'cv_policy':'reported only when a meaningful ratio scale is explicitly declared and mean > 0','quantile_method':'linear; NumPy default, one of several conventions'}

def mean_ci(values,level=.95,sigma=None):
    x=sample(values);level_check(level)
    if sigma is not None and (not math.isfinite(sigma) or sigma<=0):raise ValueError('Known sigma must be positive')
    se=(x.std(ddof=1) if sigma is None else sigma)/math.sqrt(len(x))
    if se<=0:raise ValueError('Positive standard error required')
    df=len(x)-1;critical=stats.t.ppf((1+level)/2,df) if sigma is None else stats.norm.ppf((1+level)/2)
    return {'estimate':x.mean(),'se':se,'df':df if sigma is None else None,'level':level,'method':'t' if sigma is None else 'z-known-sigma','ci':[x.mean()-critical*se,x.mean()+critical*se]}

def proportion_ci(k,n,level=.95,method='wilson'):
    counts(k,n);level_check(level)
    if method not in {'wilson','exact'}:raise ValueError('Use Wilson or exact Clopper-Pearson')
    ci=stats.binomtest(k,n).proportion_ci(confidence_level=level,method=method)
    return {'successes':k,'n':n,'estimate':k/n,'level':level,'method':method,'ci':[ci.low,ci.high]}

def variance_ci(values,level=.95):
    x=sample(values);level_check(level);df=len(x)-1;s2=x.var(ddof=1)
    if s2<=0:raise ValueError('Positive sample variance required')
    alpha=1-level
    return {'estimate':s2,'df':df,'ci':[df*s2/stats.chi2.ppf(1-alpha/2,df),df*s2/stats.chi2.ppf(alpha/2,df)],'assumption':'independent normal population observations'}

def sample_size_mean(sigma,margin,level=.95):
    level_check(level)
    if not np.isfinite([sigma,margin]).all() or sigma<=0 or margin<=0:raise ValueError('Positive finite sigma and margin required')
    return math.ceil((stats.norm.ppf((1+level)/2)*sigma/margin)**2)

def one_t(values,mu=0,level=.95):
    x=sample(values)
    if not math.isfinite(mu):raise ValueError('Finite null mean required')
    ci=mean_ci(x,level);result=stats.ttest_1samp(x,popmean=mu)
    return {**ci,'null_mean':mu,'difference':x.mean()-mu,'t':result.statistic,'p':result.pvalue,'alternative':'two-sided'}

def welch(x,y,level=.95):
    a=sample(x);b=sample(y);level_check(level);va=a.var(ddof=1)/len(a);vb=b.var(ddof=1)/len(b);se=math.sqrt(va+vb)
    if se==0:raise ValueError('Positive Welch standard error required')
    df=(va+vb)**2/(va**2/(len(a)-1)+vb**2/(len(b)-1));difference=a.mean()-b.mean();critical=stats.t.ppf((1+level)/2,df)
    result=stats.ttest_ind(a,b,equal_var=False)
    return {'n':[len(a),len(b)],'difference_A_minus_B':difference,'se':se,'df':df,'t':result.statistic,'p':result.pvalue,'ci':[difference-critical*se,difference+critical*se],'method':'Welch; two-sided'}

def paired(before,after,level=.95):
    a=sample(before);b=sample(after)
    if len(a)!=len(b):raise ValueError('Matched observations required')
    result=one_t(b-a,0,level);result['direction']='after minus before';return result

def z_power(n,delta,sigma=1,alpha=.05):
    if isinstance(n,bool) or not isinstance(n,(int,np.integer)) or n<1 or not np.isfinite([delta,sigma]).all() or sigma<=0 or not 0<alpha<1:raise ValueError('Invalid normal-power design')
    critical=stats.norm.ppf(1-alpha/2);shift=delta*math.sqrt(n)/sigma
    return float(stats.norm.cdf(-critical-shift)+stats.norm.sf(critical-shift))

def variance_test(values,sigma2=1):
    x=sample(values)
    if not math.isfinite(sigma2) or sigma2<=0:raise ValueError('Positive null variance required')
    df=len(x)-1;q=df*x.var(ddof=1)/sigma2
    return {'chi2':q,'df':df,'p':min(1.,2*min(stats.chi2.cdf(q,df),stats.chi2.sf(q,df))),'assumption':'normal population; independent observations'}

def variance_ratio(x,y):
    a=sample(x);b=sample(y)
    if min(a.var(ddof=1),b.var(ddof=1))<=0:raise ValueError('Positive variances required')
    f=a.var(ddof=1)/b.var(ddof=1);df=[len(a)-1,len(b)-1];lev=stats.levene(a,b,center='median')
    return {'F_A_over_B':f,'df':df,'p_normal_F':min(1.,2*min(stats.f.cdf(f,*df),stats.f.sf(f,*df))),
            'brown_forsythe_p':lev.pvalue,'note':'F requires independent normal samples; median-centered Levene is a different robust test'}

def contingency(table):
    x=np.asarray(table)
    if x.ndim!=2 or min(x.shape)<2 or not np.isfinite(x).all() or (x<0).any() or (x!=np.floor(x)).any() or (x.sum(0)==0).any() or (x.sum(1)==0).any():raise ValueError('Nonnegative integer counts with nonzero margins required')
    result=stats.chi2_contingency(x,correction=False);n=x.sum()
    return {'chi2':result.statistic,'df':result.dof,'p':result.pvalue,'expected':result.expected_freq,'n':n,
        'cramers_v':math.sqrt(result.statistic/(n*min(x.shape[0]-1,x.shape[1]-1))),
        'expected_below_5':int((result.expected_freq<5).sum()),'correction':'none; Pearson statistic'}

def one_way(groups,equal_var=True):
    if len(groups)<2:raise ValueError('At least two independent groups required')
    values=[sample(g) for g in groups]
    if any(np.var(g,ddof=1)<=0 for g in values):raise ValueError('Positive within-group variances required')
    total=np.concatenate(values);grand=total.mean();ssb=sum(len(g)*(g.mean()-grand)**2 for g in values);ssw=sum(((g-g.mean())**2).sum() for g in values)
    result=stats.f_oneway(*values,equal_var=equal_var)
    return {'method':'classical' if equal_var else 'Welch','F':result.statistic,'p':result.pvalue,
       'group_n':[len(g) for g in values],'group_means':[g.mean() for g in values],
       'classical_sums_of_squares':{'between':ssb,'within':ssw,'total':ssb+ssw},'descriptive_eta_squared':ssb/(ssb+ssw)}

def posthoc(groups,use_var='equal'):
    if use_var not in {'equal','unequal'} or len(groups)<2:raise ValueError('Invalid posthoc design')
    arrays=[sample(g) for g in groups];labels=np.concatenate([[f'G{i+1}']*len(g) for i,g in enumerate(arrays)])
    result=pairwise_tukeyhsd(np.concatenate(arrays),labels,use_var=use_var)
    return {'method':'Tukey HSD' if use_var=='equal' else 'Games-Howell','direction':'second group minus first group',
       'pairs':[[str(a),str(b)] for i,a in enumerate(result.groupsunique) for b in result.groupsunique[i+1:]],
       'differences':result.meandiffs,'adjusted_p':result.pvalues,'simultaneous_ci':result.confint,'reject':result.reject}

def factorial_data(interaction=True):
    rng=np.random.default_rng(SEED);records=[]
    for a in ['A0','A1']:
        for b in ['B0','B1','B2']:
            for _ in range(8):
                effect={'B0':0,'B1':2,'B2':4}[b]
                value=20+3*(a=='A1')+effect+4*(interaction and a=='A1' and b=='B2')+rng.normal(0,1)
                records.append({'A':a,'B':b,'y':value})
    return pd.DataFrame(records)

def factorial(interaction=True):
    data=factorial_data(interaction);formula='y ~ C(A)*C(B)' if interaction else 'y ~ C(A)+C(B)'
    model=smf.ols(formula,data=data).fit();table=sm.stats.anova_lm(model,typ=2)
    # Residual row has no F/p; avoid misleading fake zeros and invalid JSON NaN.
    rows={str(name):{str(key):(float(value) if pd.notna(value) else None) for key,value in row.items()} for name,row in table.iterrows()}
    return {'formula':formula,'n':len(data),'cell_n':8,'anova_type':2,'table':rows,'data_generator_has_interaction':interaction,'note':'balanced, replicated synthetic design; different data mechanisms for additive and interaction examples'}

def regression_data():
    x=np.arange(1.,21.);rng=np.random.default_rng(SEED)
    return x,3+1.7*x+rng.normal(0,2,len(x))

def regression(x=None,y=None):
    if x is None:x,y=regression_data()
    a=sample(x,3);b=sample(y,3)
    if len(a)!=len(b) or np.ptp(a)==0:raise ValueError('Matched observations and varying predictor required')
    model=sm.OLS(b,sm.add_constant(a),missing='raise').fit();robust=model.get_robustcov_results(cov_type='HC3')
    prediction=model.get_prediction([[1,float(a.mean())]]).summary_frame(alpha=.05).iloc[0]
    return {'n':len(a),'coefficients_intercept_slope':model.params,'coefficient_ci':model.conf_int(),'p_slope':model.pvalues[1],
       'r_squared':model.rsquared,'residual_df':model.df_resid,'residual_sd':math.sqrt(model.mse_resid),
       'HC3_se':robust.bse,'classical_se':model.bse,'prediction_at_mean_x':prediction.to_dict(),
       'max_cooks_distance':model.get_influence().cooks_distance[0].max(),'residuals':model.resid}

def load_survey(path=None):
    source=Path(path) if path else Path(__file__).resolve().parent/'data/survey.csv'
    data=pd.read_csv(source);required=['id','group','category','q1','q2','q3_negative','q4','q5','q6','before','after']
    if list(data.columns)!=required or data['id'].isna().any() or data['id'].duplicated().any():raise ValueError('Expected survey schema and unique IDs')
    if not data['group'].isin(['A','B','C']).all() or not data['category'].isin(['X','Y']).all():raise ValueError('Unknown category')
    for col in ['q1','q2','q3_negative','q4','q5','q6']:
        data[col]=pd.to_numeric(data[col],errors='raise');valid=data[col].dropna()
        if not valid.between(1,5).all() or not np.equal(valid,np.floor(valid)).all():raise ValueError('Likert item must be integer 1..5 or missing')
    for col in ['before','after']:
        data[col]=pd.to_numeric(data[col],errors='raise')
        if not np.isfinite(data[col].to_numpy()).all():raise ValueError('Finite paired scores required')
    data['q3']=6-data['q3_negative']
    data['service']=data[['q1','q2','q3']].mean(axis=1).where(data[['q1','q2','q3']].notna().sum(axis=1)>=2)
    return data

def alpha_reliability(items):
    x=np.asarray(items,dtype=float)
    if x.ndim!=2 or x.shape[0]<3 or x.shape[1]<2 or not np.isfinite(x).all():raise ValueError('Complete finite item matrix required; choose missing policy explicitly')
    variance=x.sum(axis=1).var(ddof=1)
    if variance<=0:raise ValueError('Positive total-score variance required')
    k=x.shape[1];return float(k/(k-1)*(1-x.var(axis=0,ddof=1).sum()/variance))

def factor_report(items):
    x=np.asarray(items,dtype=float)
    if x.ndim!=2 or x.shape[1]<3 or x.shape[0]<=x.shape[1]+2 or not np.isfinite(x).all() or (x.std(axis=0)==0).any():raise ValueError('Complete finite matrix with sufficient observations required')
    correlation=np.corrcoef(x,rowvar=False);sign,logdet=np.linalg.slogdet(correlation)
    if sign<=0 or np.linalg.eigvalsh(correlation).min()<1e-8:raise ValueError('Nonsingular correlation matrix required')
    inverse=np.linalg.inv(correlation);partial=-inverse/np.sqrt(np.outer(inverse.diagonal(),inverse.diagonal()))
    np.fill_diagonal(correlation,0);np.fill_diagonal(partial,0)
    kmo=(correlation**2).sum()/((correlation**2).sum()+(partial**2).sum())
    n,p=x.shape;statistic=-(n-1-(2*p+5)/6)*logdet;df=p*(p-1)//2
    fitted=Factor(x,n_factor=2,method='pa').fit();fitted.rotate('varimax')
    return {'n_complete':n,'n_items':p,'extraction':'principal axis; two factors fixed for demonstration','rotation':'varimax; orthogonal',
       'kmo':kmo,'bartlett_chi2':statistic,'bartlett_df':df,'bartlett_p':stats.chi2.sf(statistic,df),
       'loadings':fitted.loadings,'communalities':(fitted.loadings**2).sum(axis=1),
       'limit':'Pearson correlations for Likert items are an approximation; not PCA, CFA or proof of validity'}

def survey_report():
    data=load_survey();items=data[['q1','q2','q3']].dropna();scores=data['service'].dropna()
    grouped=[data.loc[data.group==group,'service'].dropna().to_numpy() for group in ['A','B','C']]
    all_items=data[['q1','q2','q3','q4','q5','q6']].dropna()
    return {'versions':{'numpy':np.__version__,'scipy':scipy.__version__,'pandas':pd.__version__,'statsmodels':statsmodels.__version__},
       'scope':'synthetic teaching survey; no representative sampling or causal claim','n_rows':len(data),'group_order':['A','B','C'],
       'scoring':'q3 = 6 - q3_negative; mean of service items requires >=2/3 responses',
       'descriptives':describe(scores),'reliability':{'alpha':alpha_reliability(items),'n_complete':len(items)},
       'factor_analysis':factor_report(all_items),'welch_A_minus_B':welch(grouped[0],grouped[1]),
       'paired_after_minus_before':paired(data.before,data.after),'welch_anova':one_way(grouped,equal_var=False),
       'games_howell':posthoc(grouped,use_var='unequal'),
       'interpretation':'Exploratory collection of demonstrations. Confirmatory analysis requires prespecified family-wise testing and fresh evidence.'}

def save_report(path,report):
    destination=Path(path)
    def convert(x):
        if isinstance(x,np.ndarray):return x.tolist()
        if isinstance(x,np.generic):return x.item()
        raise TypeError(type(x).__name__)
    content=json.dumps(report,default=convert,allow_nan=False,ensure_ascii=False,indent=2)
    destination.parent.mkdir(parents=True,exist_ok=True)
    with destination.open('x',encoding='utf-8') as handle:handle.write(content+'\n')
