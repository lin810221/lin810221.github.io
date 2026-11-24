"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from lm_core import filter_logits,print_json

def main():
    logits=torch.tensor([3.,2.,1.,0.])
    policies={}
    for name,options in [('temperature2',{'temperature':2.}),('topk2',{'top_k':2}),('topp.8',{'top_p':.8})]:
        filtered=filter_logits(logits,**options)
        policies[name]={'probabilities':filtered.softmax(-1).tolist(),'allowed':torch.isfinite(filtered).tolist()}
    print_json(policies)

if __name__=='__main__':main()
