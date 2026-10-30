"""Broadcasting is real tensor arithmetic; accepted shapes may still be wrong."""
import json
import torch

def main(argv=None):
    del argv
    prediction = torch.zeros(4, 1)
    target = torch.arange(4, dtype=torch.float32)
    result = {"prediction": list(prediction.shape), "target": list(target.shape),
              "wrong_difference": list((prediction-target).shape),
              "correct_difference": list((prediction-target.unsqueeze(1)).shape),
              "keepdim_mean": list(prediction.mean(dim=0, keepdim=True).shape)}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
