"""A scalar loss with hand-checkable gradient; two fresh forwards accumulate."""
import json
import torch

def main(argv=None):
    del argv
    w = torch.tensor(2., requires_grad=True)
    loss = (w * 3 - 10).square()
    loss.backward()
    first = w.grad.item()
    (w * 3 - 10).square().backward()
    accumulated = w.grad.item()
    w.grad = None
    (w * 3 - 10).square().backward()
    result = {"loss": loss.item(), "gradient": first, "accumulated_gradient": accumulated,
              "after_clear": w.grad.item(), "hand_gradient": 2 * (2 * 3 - 10) * 3}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
