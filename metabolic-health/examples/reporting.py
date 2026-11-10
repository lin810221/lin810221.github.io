"""A standalone educational report preserving clinical context and missingness."""
from pathlib import Path
from hashlib import sha256
import csv,json,platform
from metabolic_data import DATA,bp_summary,visits,visit_arithmetic

def bp_svg(summary):
    title='Synthetic BP observations: available daily means, not diagnosis'
    pieces=[]
    for i,(day,row) in enumerate(summary['daily'].items()):
        y=55+i*31;value=row['available_sbp_mean'];count=row['observed_pairs']
        pieces.append(f'<text x="15" y="{y+15}">Day {day}</text>')
        if value is None:pieces.append(f'<text x="95" y="{y+15}">unknown</text>')
        else:pieces.append(f'<rect x="95" y="{y}" width="{value/160*300:.3f}" height="20" fill="#397354"/><text x="410" y="{y+15}">{value:.1f} mmHg; n={count}/4</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 315" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">Fictional systolic observations; incomplete days remain labeled. No personal goal or risk classification.</desc><rect width="650" height="315" fill="white"/><g fill="#222" font-family="sans-serif" font-size="13"><text x="15" y="25">{title}</text>{"".join(pieces)}<text x="15" y="300">Available observations only. Missing is not normal. No diagnostic threshold line.</text></g></svg>'

def deliver(destination):
    dest=Path(destination);dest.mkdir(parents=True,exist_ok=False)
    bp=bp_summary();derived=[visit_arithmetic(v) for v in visits()]
    with (dest/'observations.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(derived[0]));writer.writeheader();writer.writerows(derived)
    (dest/'bp_observations.svg').write_text(bp_svg(bp),encoding='utf-8')
    report={'synthetic':True,'checked':'2026-11-10','python':platform.python_version(),
            'data_sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(DATA.iterdir()) if p.is_file()},
            'bp_summary':bp,'derived_observations':derived,
            'sources':json.loads((DATA/'sources.json').read_text(encoding='utf-8')),
            'checks':{'incomplete_bp_preserved':bp['complete_mean'] is None,'missing_lipid_not_zero':derived[2]['non_hdl_mg_dl'] is None},
            'scope':'Fictional arithmetic and source audit, not a diagnosis, risk score, screening recommendation or medication instruction'}
    (dest/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return {'output':str(dest),'checks':report['checks'],'scope':report['scope']}
