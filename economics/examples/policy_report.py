"""Generate a standalone CSV, SVG and JSON policy exercise. No third-party packages."""
from pathlib import Path
from hashlib import sha256
from xml.sax.saxutils import escape
import csv
import json
import platform
from microeconomics import market
from evidence import DATA


def market_svg(a=100,b=1,c=20,d=1,tax=20):
    result=market(a,b,c,d,tax)
    baseline=market(a,b,c,d)
    qmax=1.12*(a-c)/(b+d); pmax=1.1*a
    x=lambda q:55+q/qmax*560
    y=lambda p:325-p/pmax*280
    point=lambda q,p:f'{x(q):.3f},{y(p):.3f}'
    demand=f'{point(0,a)} {point(qmax,a-b*qmax)}'
    supply=f'{point(0,c)} {point(qmax,c+d*qmax)}'
    wedge=''
    if result['q']:
        q=result['q']; pb=result['buyer_price']; ps=result['seller_price']
        wedge=f'<path d="M{x(q):.3f} {y(pb):.3f}V{y(ps):.3f}" stroke="#a96400" stroke-width="5"/><text x="{x(q)+10:.3f}" y="{y(pb)+18:.3f}">tax = {tax:g}</text>'
    title=escape('Synthetic competitive market: unit tax and traded quantity')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 400" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">Fictional inverse demand P={a}-{b}Q and supply P={c}+{d}Q. Baseline Q={baseline['q']:.3f}; taxed Q={result['q']:.3f}. No empirical calibration.</desc><rect width="680" height="400" fill="white"/><g font-family="sans-serif" font-size="13" fill="#222"><text x="55" y="24">{title}</text><path d="M55 40V325H625" fill="none" stroke="#222"/><text x="22" y="55">P</text><text x="625" y="347">Q</text><text x="52" y="347">0</text><polyline points="{demand}" fill="none" stroke="#17619b" stroke-width="2"/><polyline points="{supply}" fill="none" stroke="#227c46" stroke-width="2"/>{wedge}<text x="490" y="65" fill="#17619b">Demand</text><text x="490" y="88" fill="#227c46">Supply</text><text x="55" y="375">Teaching model. Quantity, price and welfare use explicit fictional units.</text></g></svg>'''


def deliver(destination):
    destination=Path(destination)
    destination.mkdir(parents=True,exist_ok=False)
    rows=[]
    for name,slope in [('flatter_demand',.5),('baseline',1),('steeper_demand',2)]:
        # Different slopes also change the no-tax equilibrium. This is sensitivity,
        # not a clean ceteris-paribus empirical comparison of elasticity alone.
        for tax in (0,10,20,40,80): rows.append({'scenario':name,'demand_slope':slope,'tax':tax,**market(b=slope,tax=tax)})
    with (destination/'scenarios.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (destination/'market.svg').write_text(market_svg(),encoding='utf-8')
    report={'synthetic':True,'python':platform.python_version(),'checked':'2026-11-09',
            'model':'competitive linear partial equilibrium; no externalities; per-unit tax',
            'data_sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(DATA.iterdir()) if p.is_file()},
            'scenarios':len(rows),'baseline_tax20':market(tax=20),
            'checks':{'welfare_identity':all(abs(r['cs']+r['ps']+r['revenue']-r['total_surplus'])<1e-8 for r in rows),
                      'no_negative_trade':all(r['q']>=0 for r in rows)},
            'interpretation':'scenario arithmetic, not a forecast or identified policy effect'}
    (destination/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report
