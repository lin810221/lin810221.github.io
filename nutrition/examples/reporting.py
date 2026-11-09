"""A standalone composition/evidence report; no adequacy/safety score."""
from pathlib import Path
from hashlib import sha256
from xml.sax.saxutils import escape
import csv
import json
import platform
from food_data import DATA,diary,foods,meal,references
from nutrition_core import reference_percent


def svg_diary(days):
    rows=[(name,record['nutrients']['energy_kcal']['amount']) for name,record in days.items()]
    known=[value for _,value in rows if value is not None]
    maximum=max([1,*known]);parts=[]
    for i,(name,value) in enumerate(rows):
        y=65+i*62
        parts.append(f'<text x="20" y="{y+18}">{escape(name)}</text>')
        if value is None:parts.append(f'<text x="140" y="{y+18}">unknown</text>')
        else:parts.append(f'<rect x="140" y="{y}" width="{value/maximum*340:.3f}" height="25" fill="#337452"/><text x="495" y="{y+18}">{value:.1f} kcal</text>')
    title='Synthetic recorded intake: partial observations, not daily targets'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 300" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">Invented incomplete diaries. No calorie target, personal adequacy or food quality conclusion.</desc><rect width="650" height="300" fill="white"/><g fill="#222" font-family="sans-serif" font-size="13"><text x="20" y="28">{title}</text>{"".join(parts)}<text x="20" y="285">Recorded portions only. Unrecorded items and composition uncertainty remain.</text></g></svg>'


def deliver(destination):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=False)
    days=diary();rows=[]
    for day,record in days.items():
        for nutrient,result in record['nutrients'].items():
            rows.append({'day':day,'nutrient':nutrient,'amount':result['amount'],'known_subtotal':result['known_subtotal'],
                         'missing_foods':';'.join(result['missing_foods'])})
    with (destination/'recorded_nutrients.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (destination/'recorded_intake.svg').write_text(svg_diary(days),encoding='utf-8')
    sources=references()
    sample=reference_percent(400,'mg',sources['tw_label_sodium'])
    report={'synthetic':True,'python':platform.python_version(),'checked':'2026-11-09',
            'data_sha256':{path.name:sha256(path.read_bytes()).hexdigest() for path in sorted(DATA.iterdir()) if path.is_file()},
            'recorded_days':len(days),'days':days,'example_label_sodium_percent':sample,
            'checks':{'unknowns_preserved':days['day3']['nutrients']['calcium_mg']['amount'] is None,
                      'sugar_nrv_not_invented':sources['tw_label_sugars']['value'] is None},
            'interpretation':'Partial fictional diaries, not a complete menu, intake target, diagnosis or health score'}
    (destination/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return {'output':str(destination),'recorded_days':len(days),'checks':report['checks'],'scope':report['interpretation']}
