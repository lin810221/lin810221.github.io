"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from torch import nn
from lm_core import seed_everything,print_json

def main():
    seed_everything();x=torch.tensor([[[1.,2.,3.,4.],[2.,4.,6.,8.]]])
    norm=nn.LayerNorm(4,elementwise_affine=False)
    rms=nn.RMSNorm(4,elementwise_affine=False)
    ffn=nn.Sequential(nn.Linear(4,12),nn.GELU(),nn.Linear(12,4))
    print_json({'LayerNorm':norm(x).tolist(),'RMSNorm':rms(x).tolist(),
        'ffn_shape':list(ffn(x).shape),'residual_shape':list((x+ffn(norm(x))).shape)})

if __name__=='__main__':main()
