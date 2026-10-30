"""A zero residual branch preserves both values and the identity Jacobian."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    branch=nn.Linear(2,2);nn.init.zeros_(branch.weight);nn.init.zeros_(branch.bias)
    x=torch.tensor([1.,-2.],requires_grad=True)
    residual=lambda value:value+branch(value)
    jacobian=torch.autograd.functional.jacobian(residual,x)
    result={'input':x,'output':residual(x),'jacobian':jacobian,
            'note':'no post-addition ReLU here; a post-ReLU would change negative entries'}
    return emit(result)

if __name__=="__main__":
    main()
