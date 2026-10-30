"""Raw logits, class indices, binary floating targets and matched regression."""
import json
import torch
from torch.nn import functional as F

def main(argv=None):
    del argv
    logits = torch.tensor([[2., -1., 0.], [0., -1., 2.]])
    classes = torch.tensor([0, 2], dtype=torch.long)
    binary_logits = torch.tensor([[1.], [-1.]])
    binary_targets = torch.tensor([[1.], [0.]])
    prediction, target = torch.zeros(3, 1), torch.ones(3, 1)
    result = {"cross_entropy": F.cross_entropy(logits, classes).item(),
              "binary_cross_entropy": F.binary_cross_entropy_with_logits(binary_logits, binary_targets).item(),
              "mse": F.mse_loss(prediction, target).item()}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
