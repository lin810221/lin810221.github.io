"""Original offline teaching experiment; keep lm_core.py with this file."""
import copy
import torch
from lm_core import TinyGPT,make_batch,language_loss,seed_everything,print_json

def main():
    seed_everything();a=TinyGPT();b=copy.deepcopy(a)
    x,y,m=make_batch(['red bird.','blue fish moves.','a.'])
    total=int((y!=-100).sum())
    loss,_=language_loss(a(x,attention_mask=m)['logits'],y);loss.backward()
    for i in range(len(x)):
        loss,count=language_loss(b(x[i:i+1],attention_mask=m[i:i+1])['logits'],y[i:i+1])
        (loss*count/total).backward()
    error=max(float((p.grad-q.grad).abs().max()) for p,q in zip(a.parameters(),b.parameters()))
    print_json({'valid_targets':total,'max_grad_error':error,
        'policy':'sum per-token losses / total valid tokens, not mean of microbatch means'})

if __name__=='__main__':main()
