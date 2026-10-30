"""Train a tiny beta-VAE with reparameterization and analytic Gaussian KL."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import train_vae

def main(argv=None):
    del argv
    setup()
    run=train_vae()
    result={k:v for k,v in run.items() if k!='model'}
    result['scope']='beta=.1 reconstruction/KL trade-off; mean-decode MSE is not ELBO or generation quality'
    return emit(result)

if __name__=="__main__":
    main()
