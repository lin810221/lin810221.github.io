"""Compare hand-derived chain-rule gradients with real Autograd."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import manual_chain

def main(argv=None):
    del argv
    setup()
    manual=manual_chain()
    w1,b1,w2,b2=[torch.tensor(v,dtype=torch.double,requires_grad=True) for v in [.3,-.1,-.7,.2]]
    hidden=torch.sigmoid(w1*2+b1)
    loss=.5*(w2*hidden+b2-.8).square();loss.backward()
    automatic={name:value.grad.item() for name,value in [('w1',w1),('b1',b1),('w2',w2),('b2',b2)]}
    result={'manual':manual,'autograd':automatic,
            'maximum_gradient_error':max(abs(manual[k]-automatic[k]) for k in automatic)}
    return emit(result)

if __name__=="__main__":
    main()
