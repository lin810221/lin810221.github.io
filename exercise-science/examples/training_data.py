"""Fictional training records; explicit rest is zero and unobserved is unknown."""
from pathlib import Path
from datetime import date
import csv,json
from training_core import nonnegative,session_load,weekly_load,volume
DATA=Path(__file__).resolve().parent/'data'

def sessions(path=None):
    with (Path(path) if path else DATA/'sessions.csv').open(encoding='utf-8',newline='') as stream:rows=list(csv.DictReader(stream))
    seen=set()
    for row in rows:
        date.fromisoformat(row['date'])
        if row['date'] in seen:raise ValueError('One daily record per fictional day required')
        seen.add(row['date'])
        if row['status'] not in {'training','rest','missing'}:raise ValueError('Explicit daily status required')
        for key in ['minutes','srpe','moderate_minutes','vigorous_minutes']:
            row[key]=None if row[key]=='' else float(row[key])
            if row[key] is not None:nonnegative(**{key:row[key]})
        if row['srpe'] is not None and row['srpe']>10:raise ValueError('Session CR10 is 0..10')
        if row['status']=='rest' and any(row[key]!=0 for key in ['minutes','srpe','moderate_minutes','vigorous_minutes']):raise ValueError('Explicit rest has observed zero values')
        if row['status']=='missing' and any(row[key] is not None for key in ['minutes','srpe','moderate_minutes','vigorous_minutes']):raise ValueError('Missing is not observed zero')
        if row['status']=='training' and (row['minutes'] is None or row['minutes']<=0):raise ValueError('Observed training duration required')
        if all(row[key] is not None for key in ['minutes','moderate_minutes','vigorous_minutes']) and row['moderate_minutes']+row['vigorous_minutes']>row['minutes']:
            raise ValueError('Non-overlapping observed intensity minutes cannot exceed session duration')
        row['session_load_au']=None if row['minutes'] is None or row['srpe'] is None else session_load(row['minutes'],row['srpe'])
    return sorted(rows,key=lambda r:r['date'])

def weeks(path=None):
    grouped={}
    for row in sessions(path):grouped.setdefault(row['week'],[]).append(row)
    result={}
    for name,rows in sorted(grouped.items()):
        if len(rows)!=7:raise ValueError('Include seven explicit day records per week')
        dates=[date.fromisoformat(r['date']).toordinal() for r in rows]
        if dates!=list(range(dates[0],dates[0]+7)):raise ValueError('Week days must be consecutive')
        result[name]={'session_load':weekly_load([r['session_load_au'] for r in rows]),'days':rows}
    return result

def lifts(path=None):
    with (Path(path) if path else DATA/'lifts.csv').open(encoding='utf-8',newline='') as stream:rows=list(csv.DictReader(stream))
    seen=set()
    for row in rows:
        if not row['id'] or row['id'] in seen:raise ValueError('Unique set IDs required')
        seen.add(row['id'])
        if row['unit']!='kg' or not row['exercise_id']:raise ValueError('kg and exercise identity required')
        row['reps']=int(row['reps']);row['load_kg']=None if row['load_kg']=='' else float(row['load_kg'])
        row['rir']=None if row['rir']=='' else float(row['rir'])
        volume([row])
        if row['rir'] is not None and not 0<=row['rir']<=10:raise ValueError('RIR scope 0..10')
    return rows

def lift_totals(path=None):
    grouped={}
    for row in lifts(path):grouped.setdefault(row['exercise_id'],[]).append(row)
    return {exercise:volume(rows) for exercise,rows in grouped.items()}

def metadata():return json.loads((DATA/'metadata.json').read_text(encoding='utf-8'))
