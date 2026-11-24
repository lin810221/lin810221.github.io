"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from lm_core import rope,print_json

def main():
    q=torch.tensor([[[[1.,2.,3.,4.]]]],dtype=torch.float64)
    k=torch.tensor([[[[2.,1.,1.,3.]]]],dtype=torch.float64)
    qa=rope(q,torch.tensor([3]));ka=rope(k,torch.tensor([7]))
    qb=rope(q,torch.tensor([8]));kb=rope(k,torch.tensor([12]))
    print_json({'q_norm':float(q.norm()),'rotated_norm':float(qa.norm()),
        'dot_3_7':float((qa*ka).sum()),'dot_8_12':float((qb*kb).sum()),
        'convention':'adjacent dimension pairs; same relative offset'})

if __name__=='__main__':main()
