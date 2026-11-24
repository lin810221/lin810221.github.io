"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from lm_core import TinyGPT,seed_everything,print_json

def main():
    seed_everything();model=TinyGPT().eval();ids=torch.tensor([[1,30,31,32]])
    with torch.inference_mode():
        original=model(ids)['logits'][:,-1]
        changed=ids.clone();changed[0,1]=40
        altered=model(changed)['logits'][:,-1]
    print_json({'max_logit_change':float((original-altered).abs().max()),
        'scope':'controlled input perturbation in an untrained toy; not causal explanation of real-language reasoning',
        'caution':'replacement changes input distribution and may not isolate one semantic factor'})

if __name__=='__main__':main()
