"""Vectorized two-layer backward, checked against Autograd."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import softmax_gradient

def main(argv=None):
    del argv
    setup()
    x=torch.randn(3,2,dtype=torch.double)
    w1=torch.randn(2,3,dtype=torch.double,requires_grad=True)
    b1=torch.randn(3,dtype=torch.double,requires_grad=True)
    w2=torch.randn(3,2,dtype=torch.double,requires_grad=True)
    b2=torch.randn(2,dtype=torch.double,requires_grad=True)
    labels=torch.tensor([0,1,0])
    a=x@w1+b1;hidden=F.relu(a);logits=hidden@w2+b2
    loss=F.cross_entropy(logits,labels);loss.backward()
    with torch.no_grad():
        dz=softmax_gradient(logits,labels)
        da=(dz@w2.t())*(a>0)
        manual=[x.t()@da,da.sum(0),hidden.t()@dz,dz.sum(0)]
        errors=[(p.grad-g).abs().max().item() for p,g in zip([w1,b1,w2,b2],manual)]
    result={'manual_gradient_shapes':[list(g.shape) for g in manual],'maximum_error':max(errors)}
    return emit(result)

if __name__=="__main__":
    main()
