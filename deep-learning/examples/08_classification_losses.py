"""Logits-based CE/BCE and the exact softmax CE gradient."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import softmax_gradient

def main(argv=None):
    del argv
    setup()
    logits=torch.tensor([[2.,0.,-1.],[-1.,0.,2.]],requires_grad=True)
    labels=torch.tensor([0,2]);loss=F.cross_entropy(logits,labels);loss.backward()
    manual=softmax_gradient(logits.detach(),labels)
    binary_logits=torch.tensor([[2.],[-1.]])
    binary_targets=torch.tensor([[1.],[0.]])
    result={'cross_entropy':loss.item(),'probabilities':logits.softmax(1),
            'maximum_gradient_error':(manual-logits.grad).abs().max().item(),
            'bce_with_logits':F.binary_cross_entropy_with_logits(binary_logits,binary_targets).item()}
    return emit(result)

if __name__=="__main__":
    main()
