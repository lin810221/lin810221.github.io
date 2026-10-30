"""LayerNorm operates over the specified trailing dimensions."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    x=torch.randn(2,3,4);layer=nn.LayerNorm(4)
    output=layer(x)
    single=layer(x[:1]);group=nn.GroupNorm(2,4)(torch.randn(2,4,2,2))
    result={'layernorm_last_axis_means':output.mean(-1),'layernorm_batch_independence_error':(single-output[:1]).abs().max(),
            'groupnorm_output_shape':list(group.shape),'note':'LayerNorm does not use BatchNorm running means'}
    return emit(result)

if __name__=="__main__":
    main()
