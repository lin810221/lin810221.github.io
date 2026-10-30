"""He initialization preserves a ReLU second moment approximately."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    layer=nn.Linear(128,128,bias=False)
    nn.init.kaiming_normal_(layer.weight,mode='fan_in',nonlinearity='relu')
    x=torch.randn(1024,128)
    with torch.no_grad():y=F.relu(layer(x))
    result={'weight_variance':layer.weight.var(unbiased=False),'input_second_moment':x.square().mean(),
            'relu_second_moment':y.square().mean(),'relu_centered_variance':y.var(unbiased=False),
            'note':'second moment and centered variance differ because ReLU has a positive mean'}
    return emit(result)

if __name__=="__main__":
    main()
