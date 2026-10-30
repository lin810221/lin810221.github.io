"""Manual scaled dot-product attention checked against the current PyTorch API."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    q=torch.randn(1,1,3,2,dtype=torch.double)
    k=torch.randn(1,1,3,2,dtype=torch.double);v=torch.randn(1,1,3,2,dtype=torch.double)
    weights=(q@k.transpose(-2,-1)/(q.shape[-1]**.5)).softmax(-1)
    manual=weights@v
    automatic=F.scaled_dot_product_attention(q,k,v,dropout_p=0.)
    result={'weights':weights,'row_sums':weights.sum(-1),'maximum_error':(manual-automatic).abs().max()}
    return emit(result)

if __name__=="__main__":
    main()
