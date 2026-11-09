"""Transparent teaching arithmetic, not a training prescription or injury model."""
from math import isfinite,sin,radians,sqrt,exp
from statistics import mean,stdev

def nonnegative(**values):
    for name,value in values.items():
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not isfinite(value) or value<0:
            raise ValueError(f'{name}: finite nonnegative number required')

def positive(**values):
    nonnegative(**values)
    if any(v==0 for v in values.values()):raise ValueError('Positive denominator required')

def count(value,minimum=0):
    if type(value) is not int or value<minimum:raise ValueError('Integer count required')

def torque(force_n=100,lever_m=.3,angle_deg=90):
    nonnegative(force_n=force_n,lever_m=lever_m,angle_deg=angle_deg)
    if angle_deg>180:raise ValueError('Angle 0..180 degrees in this magnitude model')
    return force_n*lever_m*sin(radians(angle_deg))

def external_work(mass_kg=20,rise_m=.5,seconds=1):
    nonnegative(mass_kg=mass_kg,rise_m=rise_m);positive(seconds=seconds)
    work=mass_kg*9.80665*rise_m
    return {'joules':work,'watts':work/seconds,'scope':'Vertical external load only, not total joint work or metabolic energy'}

def impulse(force_n=200,seconds=.2):
    nonnegative(force_n=force_n,seconds=seconds)
    return force_n*seconds

def oxygen_units(absolute_ml_min=2500,mass_kg=70):
    nonnegative(absolute_ml_min=absolute_ml_min);positive(mass_kg=mass_kg)
    return absolute_ml_min/mass_kg

def cardiac_output(hr_bpm=120,stroke_ml=100):
    positive(hr_bpm=hr_bpm,stroke_ml=stroke_ml)
    return hr_bpm*stroke_ml/1000

def relative_load(load_kg=60,reference_kg=80):
    nonnegative(load_kg=load_kg);positive(reference_kg=reference_kg)
    return 100*load_kg/reference_kg

def estimated_1rm(load_kg=60,reps=5,method='epley'):
    positive(load_kg=load_kg);count(reps,1)
    if reps>10:raise ValueError('Educational scope limited to 1..10 repetitions')
    if method not in {'epley','brzycki'}:raise ValueError('Unknown formula')
    if reps==1:return load_kg
    return load_kg*(1+reps/30) if method=='epley' else load_kg*36/(37-reps)

def rir_rpe(rir=2,scale='resistance_RIR_10'):
    nonnegative(rir=rir)
    if rir>4 or scale!='resistance_RIR_10':raise ValueError('Illustration limited to RIR 0..4 on the explicitly identified resistance scale')
    return {'rpe':10-rir,'rir':rir,'scope':'A chosen RIR scale mapping, not a Borg 6-20 conversion or measured capacity'}

def volume(sets):
    total=0;reps_total=0;missing=[]
    for i,row in enumerate(sets):
        count(row['reps']);reps_total+=row['reps']
        if row.get('load_kg') is None:
            if row['reps']>0:missing.append(i)
        else:nonnegative(load_kg=row['load_kg']);total+=row['reps']*row['load_kg']
    return {'sets':len(sets),'reps':reps_total,'volume_load_kg_reps':None if missing else total,
            'known_volume_load':total,'missing_sets':missing,'scope':'External kg x repetitions; not mechanical work, muscle-specific stimulus, or comparable across exercises'}

def direct_sets(rows):
    """Count only declared primary targets; no invented universal fractional credit."""
    result={}
    for row in rows:
        count(row['sets']);target=row['primary_target']
        if not target:raise ValueError('Explicit primary target required')
        result[target]=result.get(target,0)+row['sets']
    return result

def session_load(minutes=45,srpe=5,scale='session_CR10'):
    nonnegative(minutes=minutes,srpe=srpe)
    if srpe>10 or scale!='session_CR10':raise ValueError('Session CR10 required; do not substitute set RPE or Borg 6-20')
    return minutes*srpe

def weekly_load(days):
    if len(days)!=7:raise ValueError('Exactly seven observed or explicitly missing days required')
    for value in days:
        if value is not None:nonnegative(day=value)
    known=sum(v for v in days if v is not None)
    return {'total':None if any(v is None for v in days) else known,'known_subtotal':known,
            'missing_days':[i+1 for i,v in enumerate(days) if v is None],'scope':'Rest=0, unknown=None; no safety or injury prediction'}

def load_ratio(current,prior_weeks):
    """Uncoupled: current week is NOT included in prior baseline."""
    if len(prior_weeks)!=4:raise ValueError('Four prior completed weeks required')
    for value in [current,*prior_weeks]:
        if value is not None:nonnegative(load=value)
    if current is None or any(v is None for v in prior_weeks):return {'ratio':None,'reason':'Incomplete week is not zero'}
    baseline=mean(prior_weeks)
    return {'ratio':current/baseline if baseline else None,'prior_mean':baseline,
            'scope':'Descriptive uncoupled ratio only; no safe zone or individual injury probability'}

def rolling(values,window=3):
    count(window,1);out=[]
    for i in range(len(values)):
        part=values[max(0,i-window+1):i+1]
        for value in part:
            if value is not None:nonnegative(value=value)
        out.append(mean(part) if len(part)==window and all(v is not None for v in part) else None)
    return out

def pace(distance_km=5,minutes=30):
    positive(distance_km=distance_km,minutes=minutes)
    return {'seconds_per_km':minutes*60/distance_km,'km_h':distance_km/(minutes/60)}

def intervals(repetitions=6,work_s=60,recovery_s=90,warmup_s=600,cooldown_s=300,final_recovery=False):
    count(repetitions,1);nonnegative(work_s=work_s,recovery_s=recovery_s,warmup_s=warmup_s,cooldown_s=cooldown_s)
    if type(final_recovery) is not bool:raise ValueError('Final recovery is an explicit boolean')
    recoveries=repetitions if final_recovery else repetitions-1
    return {'work_s':repetitions*work_s,'recovery_s':recoveries*recovery_s,
            'total_s':repetitions*work_s+recoveries*recovery_s+warmup_s+cooldown_s,
            'scope':'Clock arithmetic; recovery time is not automatically vigorous activity'}

def heart_reserve(rest=60,maximum=180,fraction=.6):
    positive(rest=rest,maximum=maximum);nonnegative(fraction=fraction)
    if maximum<=rest or fraction>1:raise ValueError('Maximum > resting; fraction 0..1 required')
    return {'bpm':rest+fraction*(maximum-rest),'scope':'Hypothetical supplied HR values; not an age-predicted maximum or medical clearance'}

def standard_met(met=5,mass_kg=60,minutes=30):
    nonnegative(met=met,minutes=minutes);positive(mass_kg=mass_kg)
    gross=met*3.5*mass_kg/200*minutes
    return {'gross_kcal':gross,'above_standard_rest_kcal':max(0,met-1)*3.5*mass_kg/200*minutes,
            'scope':'Standard adult MET model: 3.5mL/kg/min and 5kcal/L O2; not measured personal expenditure or a dietary allowance'}

def activity_equivalent(moderate=90,vigorous=30,population='adults_18_64'):
    nonnegative(moderate=moderate,vigorous=vigorous)
    if population!='adults_18_64':raise ValueError('This equivalence example is scoped to adults 18-64')
    return {'moderate_equivalent_minutes':moderate+2*vigorous,
            'scope':'Aerobic guideline arithmetic only; strength, balance, sedentary time and individual context remain separate'}

def measurement(before,after):
    if len(before)!=len(after) or len(before)<2:raise ValueError('At least two aligned paired measurements required')
    for value in [*before,*after]:nonnegative(measurement=value)
    differences=[b-a for a,b in zip(before,after)]
    sd=stdev(differences);sem=sd/sqrt(2)
    return {'bias':mean(differences),'sd_difference':sd,'sem_assuming_equal_error':sem,'mdc95':1.96*sqrt(2)*sem,
            'scope':'Classical paired repeatability illustration; systematic bias and generalizability must be evaluated, not a personal progress verdict'}

def change(baseline,current,lower_is_better=False):
    nonnegative(baseline=baseline,current=current)
    if type(lower_is_better) is not bool:raise ValueError('Metric direction must be explicit')
    return {'raw_change':current-baseline,'percent_change':100*(current-baseline)/baseline if baseline else None,
            'direction':'lower_is_better' if lower_is_better else 'higher_is_better'}

def progression_state(reps,rir,upper=10):
    count(upper,1)
    if len(reps)!=len(rir) or not reps:raise ValueError('Aligned sets and RIR required')
    for rep in reps:count(rep)
    for value in rir:
        if value is not None:
            nonnegative(rir=value)
            if value>10:raise ValueError('This observation example accepts RIR 0..10')
    return {'all_reach_upper':all(rep>=upper for rep in reps),
            'rir_complete':all(value is not None for value in rir),
            'scope':'Observe declared criteria; no automatic increase or assurance of readiness'}

def fitness_fatigue(loads,tau_fitness=30,tau_fatigue=5,k_fitness=.5,k_fatigue=1):
    positive(tau_fitness=tau_fitness,tau_fatigue=tau_fatigue)
    nonnegative(k_fitness=k_fitness,k_fatigue=k_fatigue)
    fit=fat=0;rows=[]
    for day,load in enumerate(loads,1):
        nonnegative(load=load)
        fit=fit*exp(-1/tau_fitness)+k_fitness*load
        fat=fat*exp(-1/tau_fatigue)+k_fatigue*load
        rows.append({'day':day,'fitness_component':fit,'fatigue_component':fat,'toy_response':fit-fat})
    return {'rows':rows,'scope':'Arbitrary uncalibrated exponential model; not readiness, adaptation, injury risk or performance prediction'}
