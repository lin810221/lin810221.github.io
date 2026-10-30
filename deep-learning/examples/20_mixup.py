"""Mix inputs and labels; soft-target CE matches weighted hard-label CE."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    x=torch.tensor([[1.,0.],[0.,1.]]);labels=torch.tensor([0,1]);permutation=torch.tensor([1,0]);lam=.25
    mixed=lam*x+(1-lam)*x[permutation]
    logits=nn.Linear(2,2)(mixed)
    soft=lam*F.one_hot(labels,2)+(1-lam)*F.one_hot(labels[permutation],2)
    weighted=lam*F.cross_entropy(logits,labels)+(1-lam)*F.cross_entropy(logits,labels[permutation])
    result={'mixed_inputs':mixed,'soft_targets':soft,'weighted_loss':weighted,
            'soft_target_loss':F.cross_entropy(logits,soft),'maximum_difference':abs(weighted.item()-F.cross_entropy(logits,soft).item())}
    return emit(result)

if __name__=="__main__":
    main()
