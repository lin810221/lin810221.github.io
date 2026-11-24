"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from torch.nn import functional as F
from lm_core import allowed_mask,reference_attention,seed_everything,print_json

def main():
    seed_everything();q=torch.randn(1,2,2,4);k=torch.randn(1,2,5,4);v=torch.randn(1,2,5,4)
    allowed=allowed_mask(2,5,past_length=3)
    expected,_=reference_attention(q,k,v,allowed)
    actual=F.scaled_dot_product_attention(q,k,v,attn_mask=allowed,dropout_p=0.,is_causal=False)
    wrong=F.scaled_dot_product_attention(q,k,v,dropout_p=0.,is_causal=True)
    print_json({'allowed_True':allowed.int().tolist(),'max_error':float((actual-expected).abs().max()),
        'upper_left_causal_diff':float((actual-wrong).abs().max())})

if __name__=='__main__':main()
