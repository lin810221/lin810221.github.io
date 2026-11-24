"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from lm_core import print_json

def main():
    # Exact one-step discrete distribution identity, not a serving engine.
    p=torch.tensor([.5,.3,.2],dtype=torch.float64)
    q=torch.tensor([.2,.5,.3],dtype=torch.float64)
    accepted=torch.minimum(p,q)
    reject=1-accepted.sum()
    residual=(p-q).clamp_min(0)
    corrected=accepted+reject*residual/residual.sum()
    print_json({'target':p.tolist(),'draft':q.tolist(),'accepted_mass':float(accepted.sum()),
        'corrected':corrected.tolist(),'max_error':float((corrected-p).abs().max()),
        'policy':'accept draft token min(1,p/q), then sample normalized positive(p-q) on rejection'})

if __name__=='__main__':main()
