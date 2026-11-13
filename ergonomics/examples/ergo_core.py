"""Transparent task arithmetic; not diagnosis, a personal lifting limit or safety certification."""
from math import isfinite,sin,cos,radians,degrees,atan2,sqrt,exp
from statistics import mean,median

def finite(**values):
    for key,value in values.items():
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not isfinite(value):raise ValueError(f'{key}: finite numeric input required')

def nonnegative(**values):
    finite(**values)
    if any(v<0 for v in values.values()):raise ValueError('Nonnegative values required')

def positive(**values):
    nonnegative(**values)
    if any(v==0 for v in values.values()):raise ValueError('Positive denominator required')

def count(**values):
    nonnegative(**values)
    if any(type(v) is not int for v in values.values()):raise ValueError('Whole counts required')

def mass_force(mass_kg=10):
    nonnegative(mass_kg=mass_kg);return mass_kg*9.80665

def moment(force_n=100,radius_m=.3,angle_deg=90):
    nonnegative(force_n=force_n,radius_m=radius_m,angle_deg=angle_deg)
    if angle_deg>180:raise ValueError('Magnitude illustration uses 0..180 degrees')
    return force_n*radius_m*sin(radians(angle_deg))

def contact_pressure(force_n=100,area_cm2=100):
    nonnegative(force_n=force_n);positive(area_cm2=area_cm2)
    return {'kpa':force_n/(area_cm2*1e-4)/1000,'scope':'Uniform external contact model, not local tissue stress, circulation or injury threshold'}

def normal_stress(force_n=100,area_mm2=50):
    nonnegative(force_n=force_n);positive(area_mm2=area_mm2)
    return {'mpa':force_n/area_mm2,'scope':'Uniform uniaxial material model; not inferred tendon or joint force'}

def engineering_strain(change_mm=1,original_mm=100):
    finite(change_mm=change_mm);positive(original_mm=original_mm);return change_mm/original_mm

def relaxation_analogy(initial=100,equilibrium=40,tau=10,steps=31):
    nonnegative(initial=initial,equilibrium=equilibrium);positive(tau=tau);count(steps=steps)
    if equilibrium>initial or not 2<=steps<=200:raise ValueError('Equilibrium <= initial and 2..200 steps required')
    return {'rows':[{'time_arbitrary':t,'value':equilibrium+(initial-equilibrium)*exp(-t/tau)} for t in range(steps)],
            'scope':'Uncalibrated exponential relaxation analogy; no human tissue healing, fatigue or injury prediction'}

def view_geometry(horizontal_cm=60,vertical_cm=-10):
    positive(horizontal_cm=horizontal_cm);finite(vertical_cm=vertical_cm)
    return {'distance_cm':sqrt(horizontal_cm**2+vertical_cm**2),'angle_deg':degrees(atan2(vertical_cm,horizontal_cm)),
            'scope':'Point-to-point geometry only, not a perfect posture angle or individual visual prescription'}

def angular_size(height_mm=4,distance_cm=60):
    positive(height_mm=height_mm,distance_cm=distance_cm)
    return {'degrees':degrees(2*atan2(height_mm/2,distance_cm*10)),'scope':'Visual-angle geometry, not visual acuity, font equivalence, eye-strain diagnosis or a viewing-distance prescription'}

def summarize(values,scale_max=None):
    values=list(values)
    for value in values:
        if value is not None:
            nonnegative(value=value)
            if scale_max is not None and value>scale_max:raise ValueError('Outside the stated original scale')
    known=[v for v in values if v is not None]
    return {'scheduled':len(values),'observed':len(known),'missing':len(values)-len(known),'known_subtotal':sum(known),
            'available_mean':mean(known) if known else None,'median':median(known) if known else None,
            'complete_total':sum(known) if len(known)==len(values) else None,
            'complete_mean':mean(known) if known and len(known)==len(values) else None}

def repetition(actions=90,observed_minutes=10,active_minutes=7):
    count(actions=actions);positive(observed_minutes=observed_minutes);nonnegative(active_minutes=active_minutes)
    if active_minutes>observed_minutes:raise ValueError('Active time cannot exceed the observed window')
    return {'actions_per_observed_minute':actions/observed_minutes,'active_fraction':active_minutes/observed_minutes,
            'scope':'Defined action count and observation-window arithmetic; not ART score, tissue dose, RNLE frequency protocol or injury probability'}

def schedule(work_minutes=50,change_minutes=10,cycles=4):
    nonnegative(work_minutes=work_minutes,change_minutes=change_minutes);count(cycles=cycles)
    if cycles<1 or work_minutes+change_minutes==0:raise ValueError('Positive number of nonempty cycles required')
    return {'task_minutes':work_minutes*cycles,'change_minutes':change_minutes*cycles,'total_minutes':(work_minutes+change_minutes)*cycles,
            'scope':'Hypothetical activity-change schedule, not a universal legal break entitlement or medical recovery prescription'}

def population_fit(rows,reach_required_cm=60,clearance_available_cm=62):
    nonnegative(reach_required_cm=reach_required_cm);positive(clearance_available_cm=clearance_available_cm)
    fit=[];unknown=[];not_fit=[]
    for row in rows:
        reach=row['reach_cm'];need=row['clearance_need_cm']
        for value in (reach,need):
            if value is not None:positive(dimension=value)
        if reach is None or need is None:unknown.append(row['id'])
        elif reach>=reach_required_cm and need<=clearance_available_cm:fit.append(row['id'])
        else:not_fit.append(row['id'])
    known=len(fit)+len(not_fit)
    return {'known_match_ids':fit,'known_nonmatch_ids':not_fit,'unknown_ids':unknown,'known_fraction':len(fit)/known if known else None,
            'scope':'Two explicit geometric constraints in a fictional sample, not population percentiles, overall comfort or design/safety certification'}

def rnle(load_kg=12,h_cm=25,v_cm=75,d_cm=50,a_deg=0,fm=.94,cm=1,conditions_verified=True):
    nonnegative(load_kg=load_kg,h_cm=h_cm,v_cm=v_cm,d_cm=d_cm,a_deg=a_deg)
    if h_cm>63 or v_cm>175 or d_cm>175 or a_deg>135:raise ValueError('Outside this RNLE geometry illustration; do not clamp to an upper bound')
    if type(conditions_verified) is not bool:raise ValueError('Applicability assumptions must be explicit')
    for multiplier in (fm,cm):
        if multiplier is not None:
            nonnegative(multiplier=multiplier)
            if multiplier>1:raise ValueError('Supplied multipliers must be 0..1 or unknown')
    factors={'HM':25/max(25,h_cm),'VM':1-.003*abs(v_cm-75),'DM':.82+4.5/max(25,d_cm),'AM':1-.0032*a_deg,'FM':fm,'CM':cm}
    rwl=23*factors['HM']*factors['VM']*factors['DM']*factors['AM']*fm*cm if conditions_verified and fm is not None and cm is not None else None
    return {'factors':factors,'rwl_kg':rwl,'li':load_kg/rwl if rwl is not None and rwl>0 else None,
            'scope':'RNLE one-endpoint formula under explicit teaching assumptions; FM/CM supplied from official tables, not automatically classified; not full applicability assessment, personal capacity, CLI or safety guarantee'}

def hav_a8(segments,day_complete=True):
    if type(day_complete) is not bool:raise ValueError('Completeness must be explicit')
    weighted=0;known=0;total_minutes=0;missing=0
    for segment in segments:
        a=segment['a_hv_m_s2'];minutes=segment['trigger_minutes']
        for value in (a,minutes):
            if value is not None:nonnegative(value=value)
        if minutes is not None:total_minutes+=minutes
        if a is None or minutes is None:missing+=1;continue
        weighted+=a*a*minutes;known+=1
    if total_minutes>1440:raise ValueError('Nonoverlapping exposure segments cannot exceed one day')
    return {'known_segments':known,'missing_segments':missing,'known_trigger_minutes':total_minutes,
            'known_subtotal_a8':sqrt(weighted/480),'complete_a8':sqrt(weighted/480) if day_complete and not missing else None,
            'scope':'Hand-arm, already frequency-weighted tri-axial resultant, actual trigger time, 8-hour reference; not raw phone acceleration, WBV, disease probability or regulatory certification'}

def horizontal_work(force_n=100,distance_m=5,seconds=10,angle_deg=0):
    nonnegative(force_n=force_n,distance_m=distance_m,angle_deg=angle_deg);positive(seconds=seconds)
    if angle_deg>90:raise ValueError('This forward-force illustration uses 0..90 degrees')
    work=force_n*cos(radians(angle_deg))*distance_m
    return {'joules':work,'watts':work/seconds,'scope':'Constant external force along horizontal displacement; not metabolism, initial push-force limits or personal injury risk'}

def coverage(record,required):
    return {'known':[k for k in required if k in record and record[k] is not None],
            'unknown':[k for k in required if k not in record or record[k] is None]}

def control_example(level='engineering'):
    examples={'elimination':'取消不必要的重複搬抬步驟，先確認任務是否可移除。','engineering':'改變物件位置、使用適當輔具或重新設計流程，並驗證新風險。',
              'administrative':'調整流程、訓練、工作安排和追蹤；不以換人承擔相同高暴露替代改善。','ppe':'依具體危害選擇適當防護，不能用護具保證不受傷或取代設計。'}
    if level not in examples:raise ValueError('Known teaching control category required')
    return {'category':level,'example':examples[level],'scope':'Original task-redesign discussion, not an official assessment score or compliance finding'}
