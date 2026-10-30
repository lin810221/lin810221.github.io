"""Symmetric in-batch InfoNCE with actual feature gradients."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import contrastive_loss

def main(argv=None):
    del argv
    setup()
    a=torch.randn(4,5,requires_grad=True);b=(a.detach()+.1*torch.randn(4,5)).requires_grad_()
    loss=contrastive_loss(a,b,.2);loss.backward()
    uniform=contrastive_loss(torch.ones(4,5),torch.ones(4,5),.2)
    result={'loss':loss,'first_view_gradient_norm':a.grad.norm(),'second_view_gradient_norm':b.grad.norm(),
            'collapsed_equal_logits_loss':uniform,'expected_uniform_loss':float(torch.log(torch.tensor(4.)))}
    return emit(result)

if __name__=="__main__":
    main()
