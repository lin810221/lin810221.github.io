"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from lm_core import reference_attention,print_json

def main():
    q=torch.tensor([[1.,0.],[0.,1.]])
    k=torch.tensor([[1.,0.],[0.,1.],[1.,1.]])
    v=torch.tensor([[2.,0.],[0.,4.],[6.,2.]])
    output,weights=reference_attention(q,k,v,torch.ones(2,3,dtype=torch.bool))
    print_json({'weights':weights.tolist(),'row_sums':weights.sum(-1).tolist(),'output':output.tolist()})

if __name__=='__main__':main()
