"""Receptive-field arithmetic checked with actual input gradients."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import receptive_field

def main(argv=None):
    del argv
    setup()
    layers=[(3,1,1),(3,2,1),(3,1,1)]
    model=nn.Sequential(nn.Conv1d(1,1,3,bias=False),nn.Conv1d(1,1,3,stride=2,bias=False),nn.Conv1d(1,1,3,bias=False))
    for layer in model:nn.init.ones_(layer.weight)
    x=torch.ones(1,1,31,requires_grad=True);model(x)[0,0,5].backward()
    support=x.grad[0,0].nonzero().flatten()
    result={'formula':receptive_field(layers),'actual_input_support':support,'actual_width':len(support)}
    return emit(result)

if __name__=="__main__":
    main()
