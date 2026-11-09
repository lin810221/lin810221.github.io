"""Transparent teaching arithmetic. No diagnosis, diet prescription or legal certification."""
from dataclasses import dataclass
from math import isfinite
from statistics import mean, stdev


def nonnegative(**values):
    for key,value in values.items():
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not isfinite(value) or value<0:
            raise ValueError(f'{key} must be a finite nonnegative number')


def positive(**values):
    nonnegative(**values)
    if any(value==0 for value in values.values()): raise ValueError('Positive denominator required')


MASS_IN_G={'g':1,'mg':.001,'ug':.000001}
def mass(value,source='mg',target='g'):
    nonnegative(value=value)
    if source not in MASS_IN_G or target not in MASS_IN_G: raise ValueError('Use g, mg or ug; IU is nutrient/form specific')
    return value*MASS_IN_G[source]/MASS_IN_G[target]


def sodium_salt(sodium_mg):
    nonnegative(sodium_mg=sodium_mg)
    return {'sodium_mg':sodium_mg,'salt_equivalent_g_approx':sodium_mg/1000*2.5,
            'meaning':'Approximate NaCl equivalent, not proof all sodium came from table salt'}


def energy(available_carb_g=50,protein_g=20,fat_g=10,fiber_g=5,alcohol_g=0,fiber_factor=2):
    """Available carbohydrate EXCLUDES fiber. A chosen-factor model, not a label certifier."""
    nonnegative(available_carb_g=available_carb_g,protein_g=protein_g,fat_g=fat_g,fiber_g=fiber_g,alcohol_g=alcohol_g,fiber_factor=fiber_factor)
    if fiber_factor>4: raise ValueError('Explicit fiber energy factor must be between 0 and 4')
    parts={'available_carbohydrate':4*available_carb_g,'protein':4*protein_g,'fat':9*fat_g,
           'fiber':fiber_factor*fiber_g,'alcohol':7*alcohol_g}
    total=sum(parts.values())
    return {'kcal':total,'kJ':total*4.184,'parts_kcal':parts,
            'percent_energy':{key:(100*value/total if total else None) for key,value in parts.items()},
            'scope':'Selected factors; excludes unmodeled polyols/organic acids; not guaranteed legal label energy'}


def portion(per_basis,consumed,basis=100):
    nonnegative(per_basis=per_basis,consumed=consumed);positive(basis=basis)
    return per_basis*consumed/basis


def serving_label(per_serving,serving_size,consumed,package_size=None):
    nonnegative(per_serving=per_serving,consumed=consumed);positive(serving_size=serving_size)
    if package_size is not None: positive(package_size=package_size)
    return {'servings_eaten':consumed/serving_size,'amount_eaten':per_serving*consumed/serving_size,
            'per_100':per_serving/serving_size*100,
            'servings_per_package':None if package_size is None else package_size/serving_size}


def volume_mass(value,source,target,density_g_ml=None):
    nonnegative(value=value)
    if source not in {'g','mL'} or target not in {'g','mL'}: raise ValueError('Use g or mL')
    if source==target:return value
    if density_g_ml is None: raise ValueError('Crossing mass/volume requires explicit density')
    positive(density_g_ml=density_g_ml)
    return value*density_g_ml if source=='mL' else value/density_g_ml


def energy_percent(amount_g,energy_per_g,total_kcal):
    nonnegative(amount_g=amount_g,energy_per_g=energy_per_g);positive(total_kcal=total_kcal)
    return amount_g*energy_per_g/total_kcal*100


def glycemic_load(gi,available_carb_g):
    nonnegative(available_carb_g=available_carb_g)
    if gi is None:return None
    nonnegative(gi=gi)
    return gi*available_carb_g/100


def vitamin_d(value,source='IU'):
    nonnegative(value=value)
    if source=='IU':return {'ug':value/40,'IU':value}
    if source=='ug':return {'ug':value,'IU':value*40}
    raise ValueError('Vitamin D source must be IU or ug')


def vitamin_a_rae(retinol_ug=0,beta_food_ug=0,beta_supp_ug=0,alpha_food_ug=0,cryptoxanthin_food_ug=0):
    nonnegative(retinol_ug=retinol_ug,beta_food_ug=beta_food_ug,beta_supp_ug=beta_supp_ug,alpha_food_ug=alpha_food_ug,cryptoxanthin_food_ug=cryptoxanthin_food_ug)
    return {'total_rae_ug':retinol_ug+beta_food_ug/12+beta_supp_ug/2+(alpha_food_ug+cryptoxanthin_food_ug)/24,
            'preformed_retinol_ug':retinol_ug,'ul_note':'Some ULs apply to preformed vitamin A, not total carotenoid RAE'}


def folate_dfe(amount_ug,form='food_folate'):
    nonnegative(amount_ug=amount_ug)
    factors={'food_folate':1,'folic_acid_with_food':1/.6,'folic_acid_empty_stomach':2}
    if form not in factors:raise ValueError('Unknown form; no established generic conversion for 5-MTHF')
    return {'dfe_ug':amount_ug*factors[form],
            'synthetic_folic_acid_ug':0 if form=='food_folate' else amount_ug,
            'scope':'NIH/US DFE conversion; not a dosing recommendation or jurisdiction-neutral UL'}


def reference_percent(amount,unit,reference,form=None,source_scope=None):
    """Return a comparison, never an individual adequacy/safety verdict."""
    nonnegative(amount=amount)
    required={'kind','unit','value','population','jurisdiction','source','checked'}
    if not required<=reference.keys():raise ValueError('Reference metadata incomplete')
    if reference['kind'] not in {'EAR','RDA','AI','UL','NRV','CDRR'}:raise ValueError('Reference kind must be explicit')
    if reference.get('form') and reference['form']!=form:raise ValueError('Nutrient form does not match this reference')
    if reference.get('source_scope') and reference['source_scope']!=source_scope:raise ValueError('Source scope does not match this reference')
    value=reference['value']
    if value is None:return {'percent':None,'kind':reference['kind'],'reason':'No reference value established'}
    positive(value=value)
    if unit!=reference['unit']:
        if unit not in MASS_IN_G or reference['unit'] not in MASS_IN_G:raise ValueError('Incompatible units')
        amount=mass(amount,unit,reference['unit'])
    return {'percent':100*amount/value,'kind':reference['kind'],'population':reference['population'],
            'jurisdiction':reference['jurisdiction'],'interpretation':'Arithmetic only; a single day does not diagnose deficiency or establish safety'}


def scoped_total(entries,allowed_sources):
    """Same nutrient form/unit only. Missing relevant data propagates; excluded data does not."""
    selected=[entry for entry in entries if entry['source_type'] in allowed_sources]
    known=0;missing=[]
    for entry in selected:
        if entry['amount'] is None:missing.append(entry.get('name','unknown'))
        else:nonnegative(amount=entry['amount']);known+=entry['amount']
    return {'amount':None if missing else known,'known_subtotal':known,'missing':missing,
            'scope':sorted(allowed_sources)}


def rounded_interval(displayed=0,resolution=.1):
    """Plain nearest-rounding interval. NOT Taiwan's nutrient-specific legal zero rules."""
    nonnegative(displayed=displayed);positive(resolution=resolution)
    return {'lower':max(0,displayed-resolution/2),'upper_exclusive':displayed+resolution/2,
            'scope':'Mathematical rounding illustration only, not a legal zero-label assessment'}


def density_per_100kcal(nutrient_amount,kcal):
    nonnegative(nutrient_amount=nutrient_amount);positive(kcal=kcal)
    return nutrient_amount/kcal*100


def match_energy(old_kcal,new_kcal_per_100):
    nonnegative(old_kcal=old_kcal);positive(new_kcal_per_100=new_kcal_per_100)
    return old_kcal/new_kcal_per_100*100


def cooking(raw_mass_g,cooked_mass_g,nutrient_per_100_raw,retention=1):
    positive(raw_mass_g=raw_mass_g,cooked_mass_g=cooked_mass_g);nonnegative(nutrient_per_100_raw=nutrient_per_100_raw,retention=retention)
    if retention>1:raise ValueError('Retention in this single-nutrient model is 0..1; additions must be recorded separately')
    total=raw_mass_g/100*nutrient_per_100_raw*retention
    return {'yield_ratio':cooked_mass_g/raw_mass_g,'retained_total':total,'per_100_cooked':total/cooked_mass_g*100,
            'scope':'Explicit hypothetical yield/retention; does not estimate cooking safety or all nutrients'}


def repeated_days(values):
    if not values:raise ValueError('At least one day required')
    if any(value is None for value in values):return {'mean':None,'observed_days':len(values),'reason':'Missing day is not zero'}
    for value in values:nonnegative(value=value)
    return {'mean':mean(values),'sample_sd':stdev(values) if len(values)>1 else None,'observed_days':len(values),
            'interpretation':'Observed diary variation; not habitual intake distribution or adequacy probability'}


def interval_sum(per100,amount_ranges):
    if len(per100)!=len(amount_ranges):raise ValueError('Aligned values and ranges required')
    low=high=0
    for value,(a,b) in zip(per100,amount_ranges):
        nonnegative(low=a,high=b)
        if a>b:raise ValueError('Range reversed')
        if value is None:return {'lower':None,'upper':None,'reason':'Unknown composition'}
        nonnegative(value=value);low+=value*a/100;high+=value*b/100
    return {'lower':low,'upper':high,'interpretation':'Deterministic bounds, not a confidence interval'}


def risk_comparison(events_treatment,n_treatment,events_control,n_control):
    for events,n in ((events_treatment,n_treatment),(events_control,n_control)):
        if type(events) is not int or type(n) is not int or n<=0 or not 0<=events<=n:raise ValueError('Valid integer event counts and denominators required')
    pt,pc=events_treatment/n_treatment,events_control/n_control
    reduction=pc-pt
    return {'risk_treatment':pt,'risk_control':pc,'risk_ratio':pt/pc if pc else None,'absolute_reduction':reduction,
            'relative_reduction':reduction/pc if pc else None,'number_needed_exact':1/abs(reduction) if reduction else None,
            'direction':'benefit' if reduction>0 else 'harm' if reduction<0 else 'no_difference',
            'scope':'Arithmetic only; requires outcome, time horizon, uncertainty and study design for interpretation'}
