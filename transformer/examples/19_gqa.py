"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from torch.nn import functional as F
from lm_core import seed_everything,print_json

def main():
    seed_everything();q=torch.randn(1,4,3,8);k=torch.randn(1,2,3,8);v=torch.randn(1,2,3,8)
    repeated=F.scaled_dot_product_attention(q,k.repeat_interleave(2,1),v.repeat_interleave(2,1),is_causal=True)
    direct=F.scaled_dot_product_attention(q,k,v,is_causal=True,enable_gqa=True)
    print_json({'Q':list(q.shape),'K':list(k.shape),'V':list(v.shape),
        'max_error':float((repeated-direct).abs().max()),'note':'repeat is numerical reference, not memory benchmark'})

if __name__=='__main__':main()
