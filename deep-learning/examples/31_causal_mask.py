"""SDPA bool True means allowed; future values cannot affect earlier output."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    q=torch.randn(1,1,4,3);k=torch.randn(1,1,4,3);v=torch.randn(1,1,4,3)
    allowed=torch.ones(4,4,dtype=torch.bool).tril()
    output=F.scaled_dot_product_attention(q,k,v,attn_mask=allowed,dropout_p=0.)
    changed=v.clone();changed[:,:,3]+=100
    after=F.scaled_dot_product_attention(q,k,changed,attn_mask=allowed,dropout_p=0.)
    causal=F.scaled_dot_product_attention(q,k,v,is_causal=True,dropout_p=0.)
    result={'early_positions_maximum_change':(output[:,:,:3]-after[:,:,:3]).abs().max(),
            'mask_vs_is_causal_error':(causal-output).abs().max(),
            'note':'nn.MultiheadAttention bool mask uses True for blocked, the opposite convention'}
    return emit(result)

if __name__=="__main__":
    main()
