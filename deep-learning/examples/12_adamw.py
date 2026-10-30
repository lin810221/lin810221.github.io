"""Compare decoupled decay with Adam L2 at a zero data gradient."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    result={}
    for name,kind in [('Adam',torch.optim.Adam),('AdamW',torch.optim.AdamW)]:
        w=nn.Parameter(torch.tensor(2.));optimizer=kind([w],lr=.1,weight_decay=.2)
        w.grad=torch.zeros_like(w);optimizer.step()
        result[name]={'weight_after_zero_data_gradient':w.item(),
                      'note':'nonzero weight decay can move weights despite a zero data gradient'}
    return emit(result)

if __name__=="__main__":
    main()
