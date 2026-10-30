"""Train a one-dimensional bottleneck on a synthetic curved 2D dataset."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import train_autoencoder

def main(argv=None):
    del argv
    setup()
    run=train_autoencoder()
    result={k:v for k,v in run.items() if k!='model'}
    result['scope']='2D synthetic reconstruction; not a generally calibrated generative density'
    return emit(result)

if __name__=="__main__":
    main()
