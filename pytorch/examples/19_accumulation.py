"""Unequal microbatches: sum losses / actual group sample count matches full mean."""
import copy
import json
import torch
from torch import nn
from torch.nn import functional as F
from course_core import accumulated_step, setup

def main(argv=None):
    del argv
    setup()
    x, y = torch.randn(10, 4), torch.arange(10)%3
    large = nn.Linear(4, 3)
    accumulated = copy.deepcopy(large)
    first = torch.optim.SGD(large.parameters(),lr=.1)
    second = torch.optim.SGD(accumulated.parameters(),lr=.1)
    first.zero_grad(set_to_none=True)
    F.cross_entropy(large(x),y).backward()
    first.step()
    microbatches = [(x[start:start+4],y[start:start+4]) for start in range(0,len(y),4)]
    accumulated_step(accumulated,second,microbatches)
    difference = max((a-b).abs().max().item() for a,b in zip(large.parameters(),accumulated.parameters()))
    result = {"microbatch_sizes": [len(labels) for _,labels in microbatches],
              "maximum_parameter_difference": difference, "scope": "Linear model, no Dropout or BatchNorm"}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
