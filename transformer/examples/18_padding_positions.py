"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from lm_core import TinyGPT,seed_everything,print_json

def main():
    seed_everything();model=TinyGPT().eval()
    ids=torch.tensor([[1,50,51,0],[1,70,71,72]]);mask=ids!=0
    with torch.inference_mode():
        batch=model(ids,attention_mask=mask,use_cache=True)
        single=model(ids[:1,:3])['logits'][0,-1]
        correct=batch['logits'][0,int(mask[0].sum())-1]
        wrong=batch['logits'][0,-1]
        new=model(torch.tensor([[52],[73]]),cache=batch['cache'],
            attention_mask=torch.cat([mask,torch.ones(2,1,dtype=torch.bool)],1),use_cache=True)
        unpadded=model(torch.tensor([[1,50,51,52]]))['logits'][0,-1]
    print_json({'last_valid_error':float((correct-single).abs().max()),
        'wrong_pad_position_difference':float((wrong-single).abs().max()),
        'cached_after_padding_error':float((new['logits'][0,-1]-unpadded).abs().max())})

if __name__=='__main__':main()
