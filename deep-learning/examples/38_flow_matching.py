"""Train a 1D conditional velocity field and integrate with Euler steps."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import train_flow

def main(argv=None):
    del argv
    setup()
    result=train_flow()
    return emit(result)

if __name__=="__main__":
    main()
