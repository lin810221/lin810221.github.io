"""Fictional observation windows, geometric sample and RNLE teaching cases."""
from pathlib import Path
import csv,json
from ergo_core import positive,nonnegative,summarize,repetition,rnle
DATA=Path(__file__).resolve().parent/'data'

def observations(path=None):
    with (Path(path) if path else DATA/'observations.csv').open(encoding='utf-8',newline='') as stream:rows=list(csv.DictReader(stream))
    if len(rows)!=12:raise ValueError('Twelve scheduled synthetic windows required')
    for i,row in enumerate(rows,1):
        if row['id']!=f'B{i:02d}' or row['synthetic']!='true' or row['task']!='fictional_assembly_A':raise ValueError('Unique ordered fictional task slots required')
        if row['status'] not in {'observed','missing'}:raise ValueError('Explicit observation status required')
        row['scheduled_minutes']=float(row['scheduled_minutes']);positive(minutes=row['scheduled_minutes'])
        row['actions']=None if row['actions']=='' else int(row['actions'])
        row['active_minutes']=None if row['active_minutes']=='' else float(row['active_minutes'])
        if (row['actions'] is None)!=(row['status']=='missing') or (row['active_minutes'] is None)!=(row['status']=='missing'):raise ValueError('Observed pair and missing status must agree')
        if row['status']=='observed':repetition(row['actions'],row['scheduled_minutes'],row['active_minutes'])
    return rows

def observation_summary(rows=None):
    rows=observations() if rows is None else rows;known=[r for r in rows if r['status']=='observed']
    actions=sum(r['actions'] for r in known);minutes=sum(r['scheduled_minutes'] for r in known)
    complete=len(known)==len(rows)
    return {'scheduled_windows':len(rows),'observed_windows':len(known),'scheduled_minutes':sum(r['scheduled_minutes'] for r in rows),
            'observed_minutes':minutes,'known_actions':actions,'available_actions_per_minute':actions/minutes if minutes else None,
            'complete_actions':actions if complete else None,'complete_actions_per_minute':actions/minutes if complete and minutes else None,
            'scope':'Original observed action definition and explicit missing window; not injury risk, ART score or RNLE frequency classification'}

def workers(path=None):
    with (Path(path) if path else DATA/'workers.csv').open(encoding='utf-8',newline='') as stream:rows=list(csv.DictReader(stream))
    seen=set()
    for row in rows:
        if row['synthetic']!='true' or row['id'] in seen:raise ValueError('Unique fictional sample required')
        seen.add(row['id'])
        for key in ('reach_cm','clearance_need_cm'):
            row[key]=None if row[key]=='' else float(row[key])
            if row[key] is not None:positive(dimension=row[key])
    return rows

def lift_cases(path=None):
    cases=json.loads((Path(path) if path else DATA/'lift_cases.json').read_text(encoding='utf-8'));seen=set()
    for case in cases:
        if case.get('synthetic') is not True or case['id'] in seen:raise ValueError('Unique fictional lifting case required')
        seen.add(case['id']);rnle(**case['inputs'])
    return cases
