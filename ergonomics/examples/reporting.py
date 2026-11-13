"""Auditable task observations; report never certifies personal or workplace safety."""
from pathlib import Path
from hashlib import sha256
import csv,json,platform
from ergo_core import population_fit,rnle
from ergo_data import DATA,observations,observation_summary,workers,lift_cases

def observation_svg(rows):
    max_count=max([r['actions'] or 0 for r in rows]+[1]);parts=[]
    for i,row in enumerate(rows):
        x=48+i*45;value=row['actions'];parts.append(f'<text x="{x}" y="235" text-anchor="middle">{row["id"]}</text>')
        if value is None:parts.append(f'<text x="{x}" y="210" text-anchor="middle">?</text>')
        else:
            height=value/max_count*150;parts.append(f'<rect x="{x-12}" y="{215-height:.2f}" width="24" height="{height:.2f}" fill="#397354"/><text x="{x}" y="{205-height:.2f}" text-anchor="middle">{value}</text>')
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 610 285" role="img" aria-labelledby="title desc"><title id="title">Fictional task observations, not injury probability</title><desc id="desc">Twelve scheduled ten-minute windows, one missing. Bars show available defined action counts; no risk bands.</desc><rect width="610" height="285" fill="white"/><g fill="#222" font-family="sans-serif" font-size="11"><text x="16" y="25">Fictional observed actions per scheduled ten-minute window</text>'+''.join(parts)+'<text x="16" y="267">? = unobserved, not zero. No diagnosis, safety or compliance conclusion.</text></g></svg>'

def deliver(destination):
    dest=Path(destination);dest.mkdir(parents=True,exist_ok=False);rows=observations();summary=observation_summary(rows)
    with (dest/'task_observations.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['id','scheduled_minutes','actions','active_minutes','status']);writer.writeheader();writer.writerows({k:r[k] for k in writer.fieldnames} for r in rows)
    (dest/'task_observations.svg').write_text(observation_svg(rows),encoding='utf-8')
    fits=population_fit(workers());lifts={case['id']:rnle(**case['inputs']) for case in lift_cases()}
    report={'synthetic':True,'checked':'2026-11-13','python':platform.python_version(),'observations':summary,'sample_geometry':fits,'lifting_formula_examples':lifts,
      'sources':json.loads((DATA/'references.json').read_text(encoding='utf-8')),
      'data_sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(DATA.iterdir()) if p.is_file()},
      'checks':{'missing_observation_preserved':summary['complete_actions'] is None,'unknown_applicability_preserved':lifts['unknown']['rwl_kg'] is None,'sample_missing_preserved':len(fits['unknown_ids'])==2},
      'scope':'Fictional arithmetic and task discussion, not diagnosis, personal capacity, tissue load prediction, legal compliance or workplace-safety certification'}
    (dest/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');return report
