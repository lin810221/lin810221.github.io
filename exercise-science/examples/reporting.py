"""Auditable fictional training report. No readiness or injury classification."""
from pathlib import Path
from hashlib import sha256
from xml.sax.saxutils import escape
import csv,json,platform
from training_data import DATA,weeks,lift_totals,metadata

def svg_load(records):
    maximum=max([1,*[r['session_load']['known_subtotal'] for r in records.values()]])
    pieces=[]
    for i,(week,row) in enumerate(records.items()):
        y=60+i*48;load=row['session_load'];value=load['total']
        pieces.append(f'<text x="16" y="{y+16}">{escape(week)}</text>')
        if value is None:pieces.append(f'<text x="105" y="{y+16}">unknown total; known subtotal {load["known_subtotal"]:.0f} AU</text>')
        else:pieces.append(f'<rect x="105" y="{y}" width="{value/maximum*340:.2f}" height="22" fill="#397354"/><text x="460" y="{y+16}">{value:.0f} AU</text>')
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 300" role="img" aria-labelledby="title desc"><title id="title">Synthetic session load: descriptive only</title><desc id="desc">Fictional weeks. Missing days are not zero. No target, injury risk or readiness score.</desc><rect width="650" height="300" fill="white"/><g fill="#222" font-family="sans-serif" font-size="13"><text x="16" y="28">Fictional observations; missing is not rest</text>'+''.join(pieces)+'<text x="16" y="280">AU = duration x session CR10. Not a dose equivalence or safety zone.</text></g></svg>'

def deliver(destination):
    dest=Path(destination);dest.mkdir(parents=True,exist_ok=False)
    records=weeks();rows=[]
    for week,record in records.items():
        value=record['session_load']
        rows.append({'week':week,'total_au':value['total'],'known_subtotal_au':value['known_subtotal'],'missing_days':';'.join(map(str,value['missing_days']))})
    with (dest/'weekly_load.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (dest/'training_load.svg').write_text(svg_load(records),encoding='utf-8')
    report={'synthetic':True,'checked':'2026-11-09','python':platform.python_version(),'metadata':metadata(),
            'data_sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(DATA.iterdir()) if p.is_file()},
            'weeks':records,'external_lift_totals':lift_totals(),
            'checks':{'missing_not_zero':records['week4']['session_load']['total'] is None,'bodyweight_external_load_unknown':lift_totals()['pushup']['volume_load_kg_reps'] is None},
            'interpretation':'Descriptive fictional records; no prescription, diagnosis, safe-load threshold or individual prediction'}
    (dest/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return {'output':str(dest),'checks':report['checks'],'scope':report['interpretation']}
