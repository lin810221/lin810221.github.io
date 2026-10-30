"""Registered parameters/buffers differ from modules hidden in a plain list."""
import json
import torch
from torch import nn

class CenteredMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.register_buffer("center", torch.zeros(4))
        self.layers = nn.ModuleList([nn.Linear(4, 6), nn.ReLU(), nn.Linear(6, 3)])
    def forward(self, x):
        x = x - self.center
        for layer in self.layers:
            x = layer(x)
        return x

class UnregisteredExample(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = [nn.Linear(4, 3)]  # Deliberately wrong for model registration.

def main(argv=None):
    del argv
    model = CenteredMLP()
    result = {"output_shape": list(model(torch.zeros(2, 4)).shape),
              "parameters": [name for name, _ in model.named_parameters()],
              "buffers": [name for name, _ in model.named_buffers()],
              "state_keys": list(model.state_dict()),
              "unregistered_parameter_count": sum(p.numel() for p in UnregisteredExample().parameters())}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
