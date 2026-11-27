"""Explicit contracts and engineering algorithms used by the offline labs."""
from collections import Counter
from datetime import datetime,timezone,timedelta
from decimal import Decimal
import heapq

def utc(value):
    moment=datetime.fromisoformat(value.replace('Z','+00:00'))
    if moment.tzinfo is None or moment.utcoffset() is None:raise ValueError('Timezone required')
    return moment.astimezone(timezone.utc)

def cents(value):
    number=Decimal(value)
    if not number.is_finite() or number<0 or number.as_tuple().exponent < -2:raise ValueError('Finite nonnegative amount with at most two decimals required')
    return int(number*100)

def cursor_page(rows,after=None,limit=2):
    if type(limit) is not int or limit<=0:raise ValueError('Positive page size required')
    ordered=sorted(rows,key=lambda r:(utc(r['updated_at']),r['id']))
    if after is not None:ordered=[r for r in ordered if (utc(r['updated_at']),r['id'])>(utc(after[0]),after[1])]
    return ordered[:limit]

def deduplicate(rows):
    """Greatest source sequence wins; conflicting equal-sequence payloads fail."""
    winners={}
    for row in rows:
        key=row['id'];old=winners.get(key)
        if old and row['seq']==old['seq'] and row!=old:raise ValueError('Ambiguous winner')
        if old is None or row['seq']>old['seq']:winners[key]=dict(row)
    return [winners[k] for k in sorted(winners)]

def topological_sort(dependencies):
    nodes=set(dependencies)
    if any(parent not in nodes for parents in dependencies.values() for parent in parents):raise ValueError('Unknown dependency')
    incoming={node:len(set(parents)) for node,parents in dependencies.items()}
    children={node:[] for node in nodes}
    for node,parents in dependencies.items():
        for parent in set(parents):children[parent].append(node)
    ready=[node for node,count in incoming.items() if not count];heapq.heapify(ready);result=[]
    while ready:
        node=heapq.heappop(ready);result.append(node)
        for child in sorted(children[node]):
            incoming[child]-=1
            if not incoming[child]:heapq.heappush(ready,child)
    if len(result)!=len(nodes):raise ValueError('Dependency cycle')
    return result

def retry_delays(attempts,base=1,cap=8):
    if type(attempts) is not int or attempts<1 or base<=0 or cap<=0:raise ValueError('Invalid retry budget')
    return [min(cap,base*2**i) for i in range(attempts-1)]

def quality(rows,required=('id','amount_cents')):
    total=len(rows);missing=sum(any(r.get(k) is None for k in required) for r in rows)
    ids=[r.get('id') for r in rows if r.get('id') is not None]
    duplicates=sum(n-1 for n in Counter(ids).values())
    return {'rows':total,'missing_rows':missing,'known_keys':len(ids),'distinct_keys':len(set(ids)),'duplicate_excess':duplicates,
            'completeness':None if not total else (total-missing)/total,
            'uniqueness':None if not ids else len(set(ids))/len(ids)}

def validate_scd(versions):
    grouped={}
    for row in versions:
        start=utc(row['valid_from']);end=utc(row['valid_to']) if row['valid_to'] else None
        if end is not None and end<=start:raise ValueError('Invalid half-open interval')
        grouped.setdefault(row['id'],[]).append((start,end))
    for intervals in grouped.values():
        intervals.sort(key=lambda pair:pair[0])
        for (_,previous_end),(next_start,_) in zip(intervals,intervals[1:]):
            if previous_end is None or next_start<previous_end:raise ValueError('Overlapping SCD versions')
    return True

def scd_lookup(versions,key,moment):
    validate_scd(versions);when=utc(moment)
    matches=[r for r in versions if r['id']==key and utc(r['valid_from'])<=when and (r['valid_to'] is None or when<utc(r['valid_to']))]
    return matches[0] if matches else None

def freshness(now,last_event):
    delta=(utc(now)-utc(last_event)).total_seconds()
    if delta<0:raise ValueError('Future event or clock skew')
    return delta
