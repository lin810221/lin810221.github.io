"""Freeze parameters and optimize the head only; no pretrained download."""
import json
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup

def main(argv=None):
    del argv
    setup()
    backbone = nn.Sequential(nn.Linear(4, 6), nn.ReLU())
    head = nn.Linear(6, 3)
    for parameter in backbone.parameters():
        parameter.requires_grad_(False)
    model = nn.Sequential(backbone, head)
    optimizer = torch.optim.SGD(head.parameters(), lr=.1)
    before_backbone = [p.detach().clone() for p in backbone.parameters()]
    before_head = head.weight.detach().clone()
    optimizer.zero_grad(set_to_none=True)
    F.cross_entropy(model(torch.randn(8, 4)), torch.arange(8)%3).backward()
    optimizer.step()
    result = {"backbone_unchanged": all(torch.equal(a,b) for a,b in zip(before_backbone,backbone.parameters())),
              "backbone_grad_none": all(p.grad is None for p in backbone.parameters()),
              "head_changed": not torch.equal(before_head, head.weight)}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
