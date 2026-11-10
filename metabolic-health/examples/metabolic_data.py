"""Typed fictional observations; missing is unknown, not a normal result."""
from pathlib import Path
import csv,json
from datetime import date
from statistics import mean
from metabolic_core import nonnegative,positive,bmi,non_hdl,concentration
DATA=Path(__file__).resolve().parent/'data'

def bp_readings(path=None):
    with (Path(path) if path else DATA/'bp_readings.csv').open(encoding='utf-8',newline='') as stream:rows=list(csv.DictReader(stream))
    for r in rows:
        r['day']=int(r['day']);r['sequence']=int(r['sequence'])
        if r['quality'] not in {'valid','invalid'}:raise ValueError('Explicit measurement quality required')
        for key in ('sbp','dbp'):r[key]=None if r[key]=='' else float(r[key])
    return rows

def bp_summary(rows=None,exclude_first_day=False):
    rows=bp_readings() if rows is None else rows
    if type(exclude_first_day) is not bool:raise ValueError('Exclusion rule must be explicit')
    expected={(d,p,s) for d in range(1,8) for p in ('morning','evening') for s in (1,2)};indexed={}
    for row in rows:
        slot=(row['day'],row['period'],row['sequence'])
        if slot not in expected or slot in indexed:raise ValueError('Unique predefined seven-day slots required')
        if row['unit']!='mmHg' or row['quality'] not in {'valid','invalid'}:raise ValueError('mmHg and quality required')
        if (row['sbp'] is None)!=(row['dbp'] is None):raise ValueError('Missing pair cannot be averaged separately')
        if row['sbp'] is not None:
            positive(sbp=row['sbp'],dbp=row['dbp'])
            if row['sbp']<row['dbp']:raise ValueError('SBP must not be below DBP')
        indexed[slot]=row
    if set(indexed)!=expected:raise ValueError('Missing observation must retain its scheduled slot')
    selected=[r for slot,r in sorted(indexed.items()) if not (exclude_first_day and slot[0]==1)]
    known=[r for r in selected if r['quality']=='valid' and r['sbp'] is not None]
    average={key:mean(r[key] for r in known) if known else None for key in ('sbp','dbp')}
    daily={}
    for day in range(1,8):
        subset=[r for r in known if r['day']==day]
        daily[str(day)]={'observed_pairs':len(subset),'available_sbp_mean':mean(r['sbp'] for r in subset) if subset else None,
                         'available_dbp_mean':mean(r['dbp'] for r in subset) if subset else None}
    return {'expected_pairs':len(selected),'observed_pairs':len(known),'available_mean':average,
            'complete_mean':average if len(known)==len(selected) else None,'daily':daily,
            'exclude_first_day':exclude_first_day,'scope':'Fictional scheduled readings; available mean is not a complete protocol, diagnosis, emergency triage or treatment goal'}

UNITS={'glucose':'mg/dL','total_cholesterol':'mg/dL','hdl':'mg/dL','tg':'mg/dL','a1c':'NGSP_percent','creatinine':'mg/dL'}
def visits(path=None):
    rows=json.loads((Path(path) if path else DATA/'visits.json').read_text(encoding='utf-8'));seen=set()
    for row in rows:
        date.fromisoformat(row['date'])
        if row['date'] in seen or row.get('synthetic') is not True:raise ValueError('Unique fictional visits required')
        seen.add(row['date']);positive(height_cm=row['height_cm'],weight_kg=row['weight_kg'])
        for analyte,unit in UNITS.items():
            item=row['labs'][analyte]
            if item['unit']!=unit:raise ValueError('Unexpected analyte/unit combination')
            if item['value'] is not None:nonnegative(value=item['value'])
    return sorted(rows,key=lambda r:r['date'])

def visit_arithmetic(row):
    labs=row['labs'];total=labs['total_cholesterol']['value'];hdl=labs['hdl']['value'];glucose=labs['glucose']['value']
    return {'date':row['date'],'bmi_arithmetic':bmi(row['weight_kg'],row['height_cm']/100),
            'non_hdl_mg_dl':None if total is None or hdl is None else non_hdl(total,hdl),
            'glucose_mmol_l':None if glucose is None else concentration(glucose),
            'interpretation':'No diagnostic flags; recorded values are fictional and not all clinical context is available'}
