"""Small, transparent empirical exercises; accounting is not causal identification."""
from datetime import date
from pathlib import Path
import csv
from microeconomics import finite

DATA=Path(__file__).resolve().parent/'data'


def ols(x,y):
    if len(x)!=len(y) or len(x)<3: raise ValueError("At least three aligned observations required")
    for value in [*x,*y]: finite(observation=value)
    n=len(x); xb=sum(x)/n; yb=sum(y)/n
    sxx=sum((v-xb)**2 for v in x)
    if sxx==0: raise ValueError("No regressor variation")
    slope=sum((a-xb)*(b-yb) for a,b in zip(x,y))/sxx
    intercept=yb-slope*xb
    residuals=[b-intercept-slope*a for a,b in zip(x,y)]
    return {"intercept":intercept,"slope":slope,"residuals":residuals,"n":n,
            "rss":sum(r*r for r in residuals),"interpretation":"association, not an identified causal effect"}


def difference_in_differences(treated_before,treated_after,control_before,control_after):
    finite(treated_before=treated_before,treated_after=treated_after,control_before=control_before,control_after=control_after)
    return {"estimate":(treated_after-treated_before)-(control_after-control_before),
            "identification":"Requires parallel untreated trends, no anticipation and no relevant spillover; four means cannot verify these assumptions"}


def read_vintages(path=None):
    with (Path(path) if path else DATA/'synthetic_vintages.csv').open(encoding='utf-8',newline='') as stream:
        rows=list(csv.DictReader(stream))
    seen=set()
    for row in rows:
        if row['series']!='synthetic_real_output' or row['unit']!='index' or row['adjustment']!='synthetic_SA': raise ValueError("Unexpected series metadata")
        period,release=date.fromisoformat(row['period_end']),date.fromisoformat(row['release_date'])
        if release<period: raise ValueError("Release predates completed observation period")
        key=(row['series'],row['period_end'],row['release_date'])
        if key in seen: raise ValueError("Duplicate vintage observation")
        seen.add(key)
        row['value']=float(row['value']); finite(value=row['value'])
    return rows


def as_of(rows,cutoff):
    bound=date.fromisoformat(cutoff); chosen={}
    for row in rows:
        if date.fromisoformat(row['release_date'])<=bound:
            key=row['period_end']
            if key not in chosen or row['release_date']>chosen[key]['release_date']: chosen[key]=dict(row)
    return [chosen[key] for key in sorted(chosen)]


def read_basket(path=None):
    with (Path(path) if path else DATA/'synthetic_basket.csv').open(encoding='utf-8',newline='') as stream:
        rows=list(csv.DictReader(stream))
    by_period={}; seen=set()
    for row in rows:
        key=(row['period'],row['item'])
        if key in seen: raise ValueError("Duplicate item within period")
        seen.add(key)
        price,quantity=float(row['price']),float(row['quantity'])
        finite(price=price,quantity=quantity)
        if price<=0 or quantity<0: raise ValueError("Invalid price/quantity")
        by_period.setdefault(row['period'],{})[row['item']]={'price':price,'quantity':quantity}
    items=set(next(iter(by_period.values()))) if by_period else set()
    if not items or any(set(items)!=set(values) for values in by_period.values()): raise ValueError("Basket items changed; an explicit linking method is required")
    return by_period
