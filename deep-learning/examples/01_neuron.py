"""One affine neuron and its activation, with hand-checkable numbers."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    x=torch.tensor([[1.,2.]])
    w=torch.tensor([[.5,-1.]])
    b=torch.tensor([.2])
    z=F.linear(x,w,b)
    result={'x':x,'linear_score':z,'relu':F.relu(z),'sigmoid':z.sigmoid(),
            'note':'an affine score is not automatically a probability'}
    return emit(result)

if __name__=="__main__":
    main()
