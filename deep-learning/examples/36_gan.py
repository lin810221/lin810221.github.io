"""Alternate real discriminator and generator updates on 2D synthetic samples."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import train_gan

def main(argv=None):
    del argv
    setup()
    result=train_gan()
    return emit(result)

if __name__=="__main__":
    main()
