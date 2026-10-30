"""Clipping norm and sample-weighted microbatch equivalence."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
import copy

def main(argv=None):
    del argv
    setup()
    parameter=nn.Parameter(torch.zeros(2));parameter.grad=torch.tensor([3.,4.])
    norm=torch.nn.utils.clip_grad_norm_([parameter],1.)
    model=nn.Linear(4,2);other=copy.deepcopy(model)
    x=torch.randn(10,4);y=torch.arange(10)%2
    a=torch.optim.SGD(model.parameters(),lr=.1);b=torch.optim.SGD(other.parameters(),lr=.1)
    F.cross_entropy(model(x),y).backward();a.step()
    b.zero_grad(set_to_none=True)
    for start,end in [(0,4),(4,8),(8,10)]:
        (F.cross_entropy(other(x[start:end]),y[start:end],reduction='sum')/10).backward()
    b.step()
    result={'pre_clip_norm':norm,'clipped_gradient':parameter.grad,
            'maximum_update_difference':max((p-q).abs().max().item() for p,q in zip(model.parameters(),other.parameters()))}
    return emit(result)

if __name__=="__main__":
    main()
