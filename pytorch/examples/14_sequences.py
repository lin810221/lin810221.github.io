"""Mask-aware mean pooling with a learned nn.Embedding and classification head."""
import json
import torch
from torch.nn import functional as F
from course_core import SequenceClassifier, collate_sequences, setup

def main(argv=None):
    del argv
    setup()
    tokens, mask, y = collate_sequences([([1, 2], 0), ([2, 1, 3], 0), ([4, 5], 1), ([5, 4, 6], 1)])
    model = SequenceClassifier()
    optimizer = torch.optim.AdamW(model.parameters(), lr=.05)
    initial = F.cross_entropy(model(tokens, mask), y).item()
    for _ in range(30):
        optimizer.zero_grad(set_to_none=True)
        loss = F.cross_entropy(model(tokens, mask), y)
        loss.backward()
        optimizer.step()
    result = {"tokens_shape": list(tokens.shape), "initial_loss": initial,
              "final_loss": F.cross_entropy(model(tokens, mask), y).item(),
              "pad_gradient": model.embedding.weight.grad[0].tolist(),
              "scope": "Tiny invented token labels, not language understanding"}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
