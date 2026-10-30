"""A known input gradient checked with central differences."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    model=nn.Linear(2,1,bias=False)
    with torch.no_grad():model.weight.copy_(torch.tensor([[2.,-1.]]))
    x=torch.tensor([[.3,.8]],requires_grad=True)
    model(x).sum().backward();epsilon=.001
    plus=x.detach().clone();minus=x.detach().clone();plus[0,0]+=epsilon;minus[0,0]-=epsilon
    difference=((model(plus)-model(minus))/(2*epsilon)).item()
    result={'input_gradient':x.grad,'first_coordinate_finite_difference':difference,
            'scope':'local model sensitivity, not causal feature effects'}
    return emit(result)

if __name__=="__main__":
    main()
