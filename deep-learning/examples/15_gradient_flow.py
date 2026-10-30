"""Exact derivatives through scalar linear chains, not a universal network law."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    result={}
    for factor in [.5,1.,1.5]:
        x=torch.tensor(1.,dtype=torch.double,requires_grad=True);y=x
        for _ in range(20):y=factor*y
        y.backward()
        result[str(factor)]={'depth':20,'derivative':x.grad.item(),'analytic':factor**20}
    return emit(result)

if __name__=="__main__":
    main()
