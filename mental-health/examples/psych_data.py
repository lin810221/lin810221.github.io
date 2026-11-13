"""Synthetic records with explicit missing observations and no personal identifiers."""
from pathlib import Path
from datetime import date
import csv,json
from psych_core import nonnegative,diary_summary,rolling,work_ledger
DATA=Path(__file__).resolve().parent/'data'

def diary(path=None):
    with (Path(path) if path else DATA/'diary.csv').open(encoding='utf-8',newline='') as stream:rows=list(csv.DictReader(stream))
    if len(rows)!=14:raise ValueError('Fourteen scheduled synthetic days required')
    dates=[]
    for row in rows:
        day=date.fromisoformat(row['date']);dates.append(day)
        if row['synthetic']!='true' or row['scale']!='original_diary_0_10':raise ValueError('Fictional original diary only')
        if row['status'] not in {'observed','missing'}:raise ValueError('Explicit observation status required')
        row['rating']=None if row['rating']=='' else float(row['rating'])
        if (row['rating'] is None)!=(row['status']=='missing'):raise ValueError('Rating and observation status must agree')
        diary_summary([row['rating']])
        for key in ('activity_minutes','window_minutes'):
            row[key]=None if row[key]=='' else float(row[key])
            if row[key] is not None:nonnegative(**{key:row[key]})
        if row['window_minutes'] is not None and row['window_minutes']>1440:raise ValueError('Time window exceeds one day')
    if len(set(dates))!=14 or any((b-a).days!=1 for a,b in zip(dates,dates[1:])):raise ValueError('Chronological daily slots must be consecutive and unique')
    return rows

def diary_arithmetic(rows=None):
    rows=diary() if rows is None else rows;values=[r['rating'] for r in rows]
    return {'summary':diary_summary(values),'rolling_3':rolling(values,3),'scope':'Two missing observations remain unknown; averages do not assess mental health or treatment effect'}

def workdays(path=None):
    records=json.loads((Path(path) if path else DATA/'workdays.json').read_text(encoding='utf-8'));seen=set()
    for record in records:
        if record.get('synthetic') is not True or record['id'] in seen:raise ValueError('Unique fictional workday required')
        seen.add(record['id']);work_ledger(record['available_minutes'],record['planned_task_minutes'],record['overhead_minutes'])
    return records
