"""Train a tiny CNN on generated horizontal/vertical bands. No downloads."""
import json
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup

def main(argv=None):
    del argv
    setup()
    generator = torch.Generator().manual_seed(17)
    images = torch.randn(32, 1, 8, 8, generator=generator)*.05
    labels = torch.arange(32) % 2
    images[labels == 0, :, 3:5, :] += 1
    images[labels == 1, :, :, 3:5] += 1
    model = nn.Sequential(nn.Conv2d(1, 4, 3, padding=1), nn.ReLU(), nn.Flatten(), nn.Linear(4*8*8, 2))
    optimizer = torch.optim.SGD(model.parameters(), lr=.2)
    initial = F.cross_entropy(model(images), labels).item()
    for _ in range(25):
        optimizer.zero_grad(set_to_none=True)
        loss = F.cross_entropy(model(images), labels)
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.inference_mode():
        logits = model(images)
    result = {"input_shape": list(images.shape), "output_shape": list(logits.shape),
              "initial_loss": initial, "final_loss": F.cross_entropy(logits, labels).item(),
              "training_accuracy": logits.argmax(1).eq(labels).float().mean().item(),
              "scope": "Synthetic training sanity check; not real-image accuracy"}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
