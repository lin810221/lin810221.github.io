"""Train epsilon prediction and execute a 30-step one-dimensional DDPM sampler."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import train_diffusion

def main(argv=None):
    del argv
    setup()
    result=train_diffusion()
    return emit(result)

if __name__=="__main__":
    main()
