"""Double-precision finite differences for logsumexp."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    x=torch.tensor([.2,-.4,.8],dtype=torch.double,requires_grad=True)
    passed=torch.autograd.gradcheck(lambda v:torch.logsumexp(v,0),(x,))
    gradient=torch.autograd.grad(torch.logsumexp(x,0),x)[0]
    epsilon=1e-6
    plus=x.detach().clone();minus=x.detach().clone();plus[0]+=epsilon;minus[0]-=epsilon
    finite_difference=(torch.logsumexp(plus,0)-torch.logsumexp(minus,0))/(2*epsilon)
    result={'gradcheck':passed,'gradient':gradient,'first_coordinate_difference':abs(gradient[0].item()-finite_difference.item())}
    return emit(result)

if __name__=="__main__":
    main()
