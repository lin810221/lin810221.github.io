"""Learning-rate schedules run after optimizer updates."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    w=nn.Parameter(torch.tensor(2.));optimizer=torch.optim.SGD([w],lr=.1)
    scheduler=torch.optim.lr_scheduler.StepLR(optimizer,step_size=2,gamma=.5)
    rows=[]
    for epoch in range(5):
        used_lr=optimizer.param_groups[0]['lr']
        optimizer.zero_grad(set_to_none=True);w.square().backward();optimizer.step();scheduler.step()
        rows.append({'epoch':epoch+1,'lr_used':used_lr,'weight':w.item()})
    result={'trace':rows}
    return emit(result)

if __name__=="__main__":
    main()
