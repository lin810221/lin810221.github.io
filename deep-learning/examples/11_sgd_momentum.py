"""Trace scalar SGD and momentum updates on w squared."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    result={}
    for momentum in [0.,.9]:
        w=nn.Parameter(torch.tensor(1.));optimizer=torch.optim.SGD([w],lr=.1,momentum=momentum)
        rows=[]
        for _ in range(3):
            optimizer.zero_grad(set_to_none=True);loss=w.square();loss.backward()
            gradient=w.grad.item();optimizer.step()
            rows.append({'gradient_before_step':gradient,'weight_after_step':w.item()})
        result[str(momentum)]=rows
    return emit(result)

if __name__=="__main__":
    main()
