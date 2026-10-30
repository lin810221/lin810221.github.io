"""eval changes layer behavior; no_grad/inference_mode change graph recording."""
import json
import torch
from torch import nn

def main(argv=None):
    del argv
    model = nn.Sequential(nn.Linear(4, 4), nn.Dropout(.5))
    x = torch.ones(2, 4)
    model.eval()
    recorded = model(x)
    with torch.no_grad():
        no_grad_output = model(x)
    with torch.inference_mode():
        inference_output = model(x)
    result = {"eval_still_records_grad": recorded.requires_grad,
              "no_grad_records": no_grad_output.requires_grad,
              "inference_records": inference_output.requires_grad,
              "dropout_disabled": torch.equal(no_grad_output, inference_output)}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
