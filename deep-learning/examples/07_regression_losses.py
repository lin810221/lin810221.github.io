"""MSE, MAE and Huber on the same residuals."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    target=torch.tensor([1.,2.,3.]);result={}
    for name,criterion in [('mse',F.mse_loss),('mae',F.l1_loss),('huber',F.huber_loss)]:
        prediction=torch.tensor([0.,2.,5.],requires_grad=True)
        loss=criterion(prediction,target);loss.backward()
        result[name]={'loss':loss.item(),'gradient':prediction.grad}
    return emit(result)

if __name__=="__main__":
    main()
