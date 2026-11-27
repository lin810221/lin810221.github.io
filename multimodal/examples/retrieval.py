"""Document permissions precede scoring. Toy dense features are not semantic models."""
import re
from metrics import maxsim

def chunks(document,tenant):
    return [{'id':document['sha256']+':'+str(p['page_index']),'document_sha256':document['sha256'],'tenant':tenant,'page_index':p['page_index'],'text':p['text'],'bbox':[0,0,p['width'],p['height']]} for p in document['pages']]

def lexical_search(query,rows,tenant,limit=5):
    words=set(re.findall(r'\w+',query.casefold()))
    result=[]
    for row in rows:
        if row['tenant']!=tenant:continue
        score=len(words&set(re.findall(r'\w+',row['text'].casefold())))
        if score:result.append({**row,'score':score})
    return sorted(result,key=lambda x:(-x['score'],x['id']))[:limit]

def fuse(rankings,k=60):
    if type(k) is not int or k<1:raise ValueError('Positive RRF constant required')
    scores={}
    for ranking in rankings:
        if len(ranking)!=len(set(ranking)):raise ValueError('Duplicate ids within one ranking')
        for rank,key in enumerate(ranking,1):scores[key]=scores.get(key,0)+1/(k+rank)
    return sorted(scores.items(),key=lambda x:(-x[1],x[0]))

def answer_total(document,tenant,query):
    intent=set(re.findall(r'\w+',query.casefold()))
    if 'total' not in intent or intent-{'what','is','the','invoice','total','amount','usd'}:return {'answer':None,'reason':'Question outside the bounded total-only rule'}
    hits=lexical_search(query,chunks(document,tenant),tenant)
    for hit in hits:
        match=re.search(r'(?m)^Total:\s*([0-9]+\.[0-9]{2})\s*$',hit['text'])
        if match:return {'answer':match.group(1),'page_index':hit['page_index'],'source':hit['document_sha256'],'method':'bounded regular expression over retrieved native text; no LLM'}
    return {'answer':None,'reason':'No supported evidence'}
