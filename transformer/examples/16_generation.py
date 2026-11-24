"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from lm_core import TinyGPT,Config,generate,seed_everything,print_json

def main():
    seed_everything();model=TinyGPT(Config(vocab_size=259)).eval();prompt=torch.tensor([[1,100,101]])
    a=generate(model,prompt,max_new_tokens=8,use_cache=False)
    b=generate(model,prompt,max_new_tokens=8,use_cache=True)
    sampled=generate(model,prompt,max_new_tokens=8,sample=True,top_k=8,top_p=.9)
    print_json({'greedy':a.tolist(),'cache_same_tokens':bool(torch.equal(a,b)),
                'sampled_ids':sampled.tolist(),'model':'untrained; mechanics only'})

if __name__=='__main__':main()
