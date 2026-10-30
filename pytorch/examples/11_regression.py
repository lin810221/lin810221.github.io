"""Learn y=3x+0.5 from synthetic data; target and prediction both have [N,1]."""
import json
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup

def main(argv=None):
    del argv
    setup()
    x = torch.linspace(-1, 1, 32).unsqueeze(1)
    y = 3*x + .5
    model = nn.Linear(1, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=.15)
    initial = F.mse_loss(model(x), y).item()
    for _ in range(100):
        optimizer.zero_grad(set_to_none=True)
        loss = F.mse_loss(model(x), y)
        loss.backward()
        optimizer.step()
    result = {"initial_loss": initial, "final_loss": F.mse_loss(model(x), y).item(),
              "weight": model.weight.item(), "bias": model.bias.item()}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
