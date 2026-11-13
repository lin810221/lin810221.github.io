"""Reproducible fictional observation report; no diagnosis or treatment recommendations."""
from pathlib import Path
from hashlib import sha256
import csv,json,platform
from psych_data import DATA,diary,diary_arithmetic,workdays
from psych_core import work_ledger

def diary_svg(rows):
    parts=[]
    for i,row in enumerate(rows):
        x=45+i*39;v=row['rating']
        parts.append(f'<text x="{x}" y="250" text-anchor="middle">{i+1}</text>')
        if v is None:parts.append(f'<text x="{x}" y="230" text-anchor="middle">?</text>')
        else:parts.append(f'<circle cx="{x}" cy="{225-v*17:.2f}" r="4" fill="#397354"/>')
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 630 300" role="img" aria-labelledby="title desc"><title id="title">Fictional original diary observations, not clinical assessment</title><desc id="desc">Fourteen scheduled days, missing days remain gaps; no severity bands or diagnostic threshold.</desc><rect width="630" height="300" fill="white"/><g fill="#222" font-family="sans-serif" font-size="12"><text x="15" y="24">Original ordinal diary 0..10; numeric spacing is a display convention</text><path d="M25 45V225H600" fill="none" stroke="#888"/><text x="4" y="55">10</text><text x="9" y="230">0</text>'+''.join(parts)+'<text x="20" y="283">Day index; ? = missing, not zero. No causal or safety conclusion.</text></g></svg>'

def deliver(destination):
    dest=Path(destination);dest.mkdir(parents=True,exist_ok=False);rows=diary();stats=diary_arithmetic(rows)
    with (dest/'diary_observations.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['date','rating','status','scale']);writer.writeheader();writer.writerows({k:r[k] for k in writer.fieldnames} for r in rows)
    (dest/'diary_observations.svg').write_text(diary_svg(rows),encoding='utf-8')
    plans=[work_ledger(r['available_minutes'],r['planned_task_minutes'],r['overhead_minutes']) for r in workdays()]
    report={'synthetic':True,'checked':'2026-11-13','python':platform.python_version(),'observations':stats,'work_plans':plans,
        'sources':json.loads((DATA/'sources.json').read_text(encoding='utf-8')),
        'data_sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(DATA.iterdir()) if p.is_file()},
        'checks':{'missing_preserved':stats['summary']['missing']==2 and stats['summary']['complete_mean'] is None,'unknown_plan_preserved':plans[1]['difference_minutes'] is None},
        'scope':'Fictional learning report, not diagnosis, suicide-risk prediction, treatment evaluation or fitness-for-work assessment'}
    (dest/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');return report
