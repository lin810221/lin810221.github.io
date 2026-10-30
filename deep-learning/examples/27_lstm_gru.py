"""LSTM and GRU output/state contracts with real backward."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    x=torch.randn(2,5,3);result={}
    for name,kind in [('LSTM',nn.LSTM),('GRU',nn.GRU)]:
        model=kind(3,4,batch_first=True);output,state=model(x)
        output.square().mean().backward()
        states=state if isinstance(state,tuple) else (state,)
        result[name]={'output_shape':list(output.shape),'state_shapes':[list(s.shape) for s in states],
                      'finite_gradients':all(p.grad is not None and torch.isfinite(p.grad).all().item() for p in model.parameters())}
    return emit(result)

if __name__=="__main__":
    main()
