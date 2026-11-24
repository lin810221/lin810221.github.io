"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from lm_core import make_batch,language_loss,print_json

def main():
    x,y,mask=make_batch(['a','ab'])
    logits=torch.zeros(*x.shape,259)
    nll,count=language_loss(logits,y)
    print_json({'inputs':x.tolist(),'targets':y.tolist(),'key_valid':mask.int().tolist(),
        'valid_target_tokens':count,'uniform_nll':float(nll),'expected_log259':float(torch.log(torch.tensor(259.)))})

if __name__=='__main__':main()
