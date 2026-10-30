"""Manually unroll the same weights as torch.nn.RNN."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    model=nn.RNN(1,3,batch_first=True)
    x=torch.randn(2,4,1);automatic,last=model(x)
    h=torch.zeros(2,3);rows=[]
    for t in range(x.shape[1]):
        h=torch.tanh(x[:,t]@model.weight_ih_l0.t()+model.bias_ih_l0+h@model.weight_hh_l0.t()+model.bias_hh_l0)
        rows.append(h)
    manual=torch.stack(rows,1)
    result={'output_shape':list(automatic.shape),'hidden_shape':list(last.shape),
            'manual_unroll_maximum_error':(manual-automatic).abs().max()}
    return emit(result)

if __name__=="__main__":
    main()
