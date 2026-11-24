"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from lm_core import TinyGPT,seed_everything,print_json

def main():
    seed_everything();model=TinyGPT().eval();ids=torch.tensor([[1,30,31,32,33]])
    with torch.inference_mode():
        full=model(ids)['logits']
        prefix=model(ids[:,:3],use_cache=True)
        chunk=model(ids[:,3:],cache=prefix['cache'],use_cache=True)
        error=float((full[:,3:]-chunk['logits']).abs().max())
    print_json({'past_length':3,'new_length':2,'cache_length':chunk['cache'][0][0].shape[-2],
                'max_logit_error':error,'mask':'[[1,1,1,1,0],[1,1,1,1,1]]'})

if __name__=='__main__':main()
