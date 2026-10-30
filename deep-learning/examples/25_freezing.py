"""Frozen random features demonstrate the mechanism, not pretrained transfer quality."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import snapshot

def main(argv=None):
    del argv
    setup()
    backbone=nn.Sequential(nn.Linear(4,6),nn.Tanh());head=nn.Linear(6,2)
    for p in backbone.parameters():p.requires_grad_(False)
    before=snapshot(backbone);before_head=snapshot(head)
    optimizer=torch.optim.SGD(head.parameters(),lr=.1)
    x=torch.randn(8,4);labels=torch.arange(8)%2
    with torch.no_grad():features=backbone(x)
    F.cross_entropy(head(features),labels).backward();optimizer.step()
    result={'backbone_unchanged':all(torch.equal(before[k],v) for k,v in backbone.state_dict().items()),
            'head_changed':any(not torch.equal(before_head[k],v) for k,v in head.state_dict().items()),
            'scope':'random frozen features; no pretrained model downloaded'}
    return emit(result)

if __name__=="__main__":
    main()
