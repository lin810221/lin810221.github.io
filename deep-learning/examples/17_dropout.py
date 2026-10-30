"""Inverted dropout: train scaling and eval identity."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    dropout=nn.Dropout(.5);x=torch.ones(10000)
    train=dropout(x);dropout.eval();evaluation=dropout(x)
    result={'training_mean':train.mean(),'training_unique_values':train.unique(),
            'evaluation_is_identity':torch.equal(evaluation,x),'note':'expectation is approximately preserved, not every sample'}
    return emit(result)

if __name__=="__main__":
    main()
