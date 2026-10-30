"""Batch statistics, running buffers and evaluation mode."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    x=torch.tensor([[1.,2.],[3.,4.]])
    norm=nn.BatchNorm1d(2,affine=False,momentum=.1)
    train_output=norm(x);running_mean=norm.running_mean.clone();running_variance=norm.running_var.clone()
    norm.eval();evaluation=norm(x)
    result={'training_mean':train_output.mean(0),'running_mean':running_mean,
            'running_variance':running_variance,'evaluation_output':evaluation,
            'note':'training normalization and running-variance update use different variance estimators'}
    return emit(result)

if __name__=="__main__":
    main()
