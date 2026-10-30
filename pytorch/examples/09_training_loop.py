"""A complete real optimizer update, weighted epoch metrics and parameter change."""
import json
import torch
from torch import nn
from torch.nn import functional as F
from course_core import Config, make_loaders, setup

def main(argv=None):
    del argv
    setup()
    loaders, _, _ = make_loaders(Config())
    model = nn.Linear(4, 3)
    optimizer = torch.optim.SGD(model.parameters(), lr=.1)
    before = model.weight.detach().clone()
    model.train()
    total_loss, count = 0., 0
    for x, y in loaders[0]:
        optimizer.zero_grad(set_to_none=True)
        logits = model(x)
        loss = F.cross_entropy(logits, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.detach().item() * y.numel()
        count += y.numel()
    result = {"samples": count, "mean_loss": total_loss/count,
              "weight_changed": not torch.equal(before, model.weight)}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
