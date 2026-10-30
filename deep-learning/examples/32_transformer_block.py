"""A tiny pre-norm causal block, not a pretrained language model."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import TinyBlock

def main(argv=None):
    del argv
    setup()
    model=TinyBlock().eval();x=torch.randn(2,4,8)
    position=torch.arange(4).float().reshape(1,4,1)
    x=x+torch.sin(position/torch.arange(1,9).reshape(1,1,8))
    changed=x.clone();changed[:,3]+=10
    with torch.no_grad():output=model(x);after=model(changed)
    result={'shape':list(output.shape),'early_positions_maximum_change':(output[:,:3]-after[:,:3]).abs().max(),
            'scope':'8-dimensional block with handmade position features; no tokenizer, pretraining or generation'}
    return emit(result)

if __name__=="__main__":
    main()
