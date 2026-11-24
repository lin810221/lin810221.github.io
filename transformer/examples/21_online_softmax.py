"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from lm_core import print_json

def online_weighted(scores,values,chunk=2):
    maximum=scores.new_tensor(-float('inf'));den=scores.new_tensor(0.)
    numerator=torch.zeros(values.shape[-1],dtype=values.dtype)
    for start in range(0,len(scores),chunk):
        s=scores[start:start+chunk];v=values[start:start+chunk]
        new_max=torch.maximum(maximum,s.max());rescale=torch.exp(maximum-new_max)
        e=torch.exp(s-new_max)
        numerator=numerator*rescale+(e[:,None]*v).sum(0)
        den=den*rescale+e.sum();maximum=new_max
    return numerator/den

def main():
    scores=torch.tensor([1000.,999.,1001.,997.,1002.],dtype=torch.float64)
    values=torch.arange(15,dtype=torch.float64).reshape(5,3)
    exact=scores.softmax(-1)@values;stream=online_weighted(scores,values)
    print_json({'max_error':float((exact-stream).abs().max()),'output':stream.tolist(),
        'scope':'online softmax arithmetic only; not a FlashAttention GPU kernel or speed test'})

if __name__=='__main__':main()
