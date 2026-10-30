"""Activation values and derivatives at fixed inputs."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    result={}
    for name,activation in [('sigmoid',torch.sigmoid),('tanh',torch.tanh),('relu',F.relu),('gelu',F.gelu)]:
        x=torch.tensor([-3.,-1.,0.,1.,3.],requires_grad=True)
        output=activation(x);output.sum().backward()
        result[name]={'values':output,'derivatives':x.grad}
    return emit(result)

if __name__=="__main__":
    main()
