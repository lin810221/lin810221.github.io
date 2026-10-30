"""Weighted CE normalizes by target weights, not the unweighted row count."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    logits=torch.tensor([[2.,0.],[1.,0.],[0.,1.],[0.,2.]])
    labels=torch.tensor([0,0,0,1]);weight=torch.tensor([1.,3.])
    per_row=F.cross_entropy(logits,labels,weight=weight,reduction='none')
    actual=F.cross_entropy(logits,labels,weight=weight)
    manual=per_row.sum()/weight[labels].sum()
    result={'weighted_loss':actual,'manual_loss':manual,'denominator':weight[labels].sum(),
            'note':'class weighting changes the training objective, not just the decision threshold'}
    return emit(result)

if __name__=="__main__":
    main()
