"""Transparent educational arithmetic; no diagnosis, drug dosing or personal risk model."""
from math import isfinite,sqrt,exp
from statistics import mean,stdev

def nonnegative(**values):
    for name,value in values.items():
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not isfinite(value) or value<0:raise ValueError(f'{name}: finite nonnegative number required')

def positive(**values):
    nonnegative(**values)
    if any(v==0 for v in values.values()):raise ValueError('Positive denominator required')

def probability(**values):
    nonnegative(**values)
    if any(v>1 for v in values.values()):raise ValueError('Probability must be between 0 and 1')

FACTORS={'glucose':18.0,'cholesterol':38.67,'triglycerides':88.57,'creatinine':1/88.4}
def concentration(value,analyte='glucose',source='mg/dL',target='mmol/L'):
    """Glucose 18 is a stated clinical approximation; creatinine uses umol/L."""
    nonnegative(value=value)
    if analyte not in FACTORS:raise ValueError('Specify analyte; Lp(a) mass/molar conversion has no universal factor')
    other='umol/L' if analyte=='creatinine' else 'mmol/L'
    if source not in {'mg/dL',other} or target not in {'mg/dL',other}:raise ValueError('Unit incompatible with analyte')
    if source==target:return value
    return value/FACTORS[analyte] if source=='mg/dL' else value*FACTORS[analyte]

def a1c_units(value,source='NGSP_percent'):
    nonnegative(value=value)
    if source=='NGSP_percent':
        result=(value-2.152)/.09148
        if result<0:raise ValueError('Outside nonnegative IFCC range of this conversion')
        return {'ngsp_percent':value,'ifcc_mmol_mol':result}
    if source=='IFCC_mmol_mol':return {'ngsp_percent':.09148*value+2.152,'ifcc_mmol_mol':value}
    raise ValueError('NGSP % and IFCC mmol/mol required; not blood glucose mmol/L')

def bmi(mass_kg=70,height_m=1.7):
    nonnegative(mass_kg=mass_kg);positive(height_m=height_m)
    return mass_kg/height_m**2

def waist_height(waist_cm=85,height_cm=170):
    nonnegative(waist_cm=waist_cm);positive(height_cm=height_cm)
    return waist_cm/height_cm

def change(baseline,current):
    nonnegative(baseline=baseline,current=current)
    return {'difference':current-baseline,'relative_percent':100*(current-baseline)/baseline if baseline else None,
            'scope':'Observed arithmetic; direction, measurement error and clinical meaning require context'}

def describe(values):
    for v in values:
        if v is not None:nonnegative(value=v)
    known=[v for v in values if v is not None]
    return {'observed':len(known),'missing':len(values)-len(known),'available_mean':mean(known) if known else None,
            'complete_mean':mean(known) if known and len(known)==len(values) else None,
            'sample_sd':stdev(known) if len(known)>1 else None,
            'scope':'Available observations are not a complete series or diagnosis'}

def rolling(values,window=3):
    if type(window) is not int or window<=0:raise ValueError('Positive integer window required')
    for v in values:
        if v is not None:nonnegative(value=v)
    result=[]
    for i in range(len(values)):
        part=values[max(0,i-window+1):i+1]
        result.append(mean(part) if len(part)==window and all(v is not None for v in part) else None)
    return result

def non_hdl(total_cholesterol=200,hdl=50,unit='mg/dL'):
    if unit not in {'mg/dL','mmol/L'}:raise ValueError('Cholesterol units required')
    nonnegative(total_cholesterol=total_cholesterol,hdl=hdl)
    if hdl>total_cholesterol:raise ValueError('HDL cannot exceed total cholesterol in this model')
    return total_cholesterol-hdl

def friedewald(total=200,hdl=50,tg=150,unit='mg/dL',fasting=True):
    nonnegative(total=total,hdl=hdl,tg=tg)
    if type(fasting) is not bool:raise ValueError('Fasting context required')
    if unit!='mg/dL':raise ValueError('This historical equation expects mg/dL')
    if not fasting or tg>=400:return {'ldl_estimate':None,'reason':'Outside this deliberately narrow fasting TG<400 illustration'}
    value=total-hdl-tg/5
    return {'ldl_estimate':value if value>=0 else None,'scope':'Historical approximation, not the modern default method, measured LDL or a treatment goal'}

def homa_ir(insulin_uIU_ml=8,glucose_mg_dl=100,fasting=True):
    nonnegative(insulin_uIU_ml=insulin_uIU_ml,glucose_mg_dl=glucose_mg_dl)
    if type(fasting) is not bool:raise ValueError('Fasting context required')
    return {'homa1_ir':insulin_uIU_ml*glucose_mg_dl/405 if fasting else None,
            'scope':'Historical HOMA1 approximation with modern insulin-assay calibration limitations; not HOMA2, a direct clamp measurement or a universal insulin-resistance diagnosis'}

def fib4(age=45,ast=25,alt=30,platelets=220,stable_adult=True):
    nonnegative(age=age,ast=ast);positive(alt=alt,platelets=platelets)
    if age<18 or type(stable_adult) is not bool:raise ValueError('Adult illustration with explicit stability context required')
    return {'fib4':age*ast/(platelets*sqrt(alt)) if stable_adult else None,
            'scope':'Age years, AST/ALT U/L, platelets 10^9/L; screening/risk-stratification arithmetic only, not fibrosis diagnosis or treatment eligibility'}

def urine_acr(albumin_mg_l=20,creatinine_g_l=1):
    nonnegative(albumin_mg_l=albumin_mg_l);positive(creatinine_g_l=creatinine_g_l)
    return {'acr_mg_g':albumin_mg_l/creatinine_g_l,
            'scope':'Same urine sample; not eGFR, total protein or confirmation of persistent kidney disease'}

def body_surface_area(height_cm=170,mass_kg=70):
    positive(height_cm=height_cm,mass_kg=mass_kg)
    return sqrt(height_cm*mass_kg/3600)

def unindex_gfr(indexed=90,bsa_m2=1.8):
    nonnegative(indexed=indexed);positive(bsa_m2=bsa_m2)
    return {'absolute_ml_min':indexed*bsa_m2/1.73,
            'scope':'Arithmetic de-indexing only; not measured GFR, CKD staging or a medication dose'}

def risk_comparison(events_t=80,n_t=1000,events_c=100,n_c=1000):
    for events,n in [(events_t,n_t),(events_c,n_c)]:
        if type(events) is not int or type(n) is not int or n<=0 or not 0<=events<=n:raise ValueError('Valid integer events and denominators required')
    pt,pc=events_t/n_t,events_c/n_c;arr=pc-pt
    return {'risk_t':pt,'risk_c':pc,'rr':pt/pc if pc else None,'absolute_reduction':arr,
            'relative_reduction':arr/pc if pc else None,'number_needed_exact':1/abs(arr) if arr else None,
            'direction':'benefit' if arr>0 else 'harm' if arr<0 else 'no_difference',
            'scope':'Specified adverse outcome and follow-up, point estimates only; no individual prediction'}

def assumed_effect(baseline_risk=.1,assumed_rr=.8):
    probability(baseline_risk=baseline_risk);nonnegative(assumed_rr=assumed_rr)
    treated=baseline_risk*assumed_rr
    if treated>1:raise ValueError('Assumed treated probability exceeds 1')
    arr=baseline_risk-treated
    return {'treated':treated,'absolute_reduction':arr,'scope':'Explicit assumed effect, not a trial estimate or personal PREVENT score'}

def screening(population=10000,prevalence=.01,sensitivity=.9,specificity=.95):
    if type(population) is not int or population<=0:raise ValueError('Positive integer population required')
    probability(prevalence=prevalence,sensitivity=sensitivity,specificity=specificity)
    affected=population*prevalence;unaffected=population-affected
    tp=affected*sensitivity;fn=affected-tp;tn=unaffected*specificity;fp=unaffected-tn
    return {'tp':tp,'fn':fn,'tn':tn,'fp':fp,'ppv':tp/(tp+fp) if tp+fp else None,'npv':tn/(tn+fn) if tn+fn else None,
            'scope':'Expected counts with assumed population/test properties; not an individual diagnostic probability or test recommendation'}

def prevent_age_scope(age=45,horizon=10):
    nonnegative(age=age)
    if type(age) is not int or type(horizon) is not int or horizon not in {10,30}:raise ValueError('Whole-year age and 10- or 30-year horizon required')
    return {'age_range_match':30<=age<=(79 if horizon==10 else 59),'horizon':horizon,
            'scope':'Age-only check for PREVENT context; no coefficients or risk calculation, no full clinical eligibility assessment or Taiwan calibration'}

def coverage(record,required):
    return {'known':[k for k in required if k in record and record[k] is not None],
            'missing':[k for k in required if k not in record or record[k] is None]}

def toy_balance(input_units=4,clearance=.1,steps=30):
    nonnegative(input_units=input_units,clearance=clearance)
    if clearance>1 or type(steps) is not int or not 1<=steps<=200:raise ValueError('Toy clearance 0..1, steps 1..200')
    state=0;rows=[]
    for t in range(steps):
        pulse=input_units if t<5 else 0
        state=state*(1-clearance)+pulse;rows.append({'step':t,'state_arbitrary':state})
    return {'rows':rows,'scope':'Uncalibrated input/clearance analogy; not glucose, insulin, weight or metabolic disease prediction'}
