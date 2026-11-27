"""Explicit denominators, document-level evaluation and algebraic retrieval models."""
import math

def edit_distance(reference,prediction):
    previous=list(range(len(prediction)+1))
    for i,a in enumerate(reference,1):
        current=[i]
        for j,b in enumerate(prediction,1):current.append(min(current[-1]+1,previous[j]+1,previous[j-1]+(a!=b)))
        previous=current
    return previous[-1]

def cer(reference,prediction):
    return edit_distance(reference,prediction)/len(reference) if reference else None

def anls(reference,prediction,threshold=.5):
    if not 0<threshold<=1:raise ValueError('Invalid threshold')
    denominator=max(len(reference),len(prediction))
    if not denominator:return 1.0
    distance=edit_distance(reference,prediction)/denominator
    return 1-distance if distance<threshold else 0.0

def prf(tp,fp,fn):
    if any(type(n) is not int or n<0 for n in (tp,fp,fn)):raise ValueError('Counts must be nonnegative integers')
    return {'precision':tp/(tp+fp) if tp+fp else None,'recall':tp/(tp+fn) if tp+fn else None,'f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None}

def cosine(a,b):
    if not a or len(a)!=len(b) or any(not math.isfinite(x) for x in [*a,*b]):raise ValueError('Finite equal-dimensional vectors required')
    na,nb=math.sqrt(sum(x*x for x in a)),math.sqrt(sum(x*x for x in b))
    if not na or not nb:raise ValueError('Zero vector has undefined cosine')
    return sum(x*y for x,y in zip(a,b))/(na*nb)

def maxsim(query_tokens,page_tokens):
    if not query_tokens or not page_tokens:raise ValueError('Nonempty token sets required')
    return sum(max(cosine(q,p) for p in page_tokens) for q in query_tokens)

def contrastive_loss(similarities,temperature=.1):
    n=len(similarities)
    if not n or any(len(r)!=n for r in similarities) or not math.isfinite(temperature) or temperature<=0:raise ValueError('Square paired matrix and positive temperature required')
    def direction(matrix):
        losses=[]
        for i,row in enumerate(matrix):
            if any(not math.isfinite(v) for v in row):raise ValueError('Nonfinite similarity')
            logits=[x/temperature for x in row];m=max(logits)
            losses.append(m+math.log(sum(math.exp(x-m) for x in logits))-logits[i])
        return sum(losses)/n
    return (direction(similarities)+direction(list(zip(*similarities))))/2

def risk_coverage(scores,correct,threshold):
    if len(scores)!=len(correct) or any(not 0<=s<=1 for s in scores) or not 0<=threshold<=1:raise ValueError('Invalid confidence fixture')
    selected=[ok for s,ok in zip(scores,correct) if s>=threshold]
    return {'coverage':len(selected)/len(scores) if scores else None,'risk':sum(not x for x in selected)/len(selected) if selected else None}
