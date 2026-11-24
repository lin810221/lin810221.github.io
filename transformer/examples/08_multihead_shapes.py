"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from lm_core import seed_everything,print_json

def main():
    seed_everything();x=torch.randn(2,5,24);heads=3;head_dim=8
    split=x.reshape(2,5,heads,head_dim).transpose(1,2)
    restored=split.transpose(1,2).contiguous().reshape(2,5,24)
    print_json({'input':list(x.shape),'per_head':list(split.shape),
        'roundtrip_exact':bool(torch.equal(x,restored)),'per_head_score_shape':[2,3,5,5]})

if __name__=='__main__':main()
