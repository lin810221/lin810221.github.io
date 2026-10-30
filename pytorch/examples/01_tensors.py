"""Real CPU tensors: dtype, shape, device and Python conversion."""
import json
import torch

def main(argv=None):
    del argv
    values = torch.tensor([[1., 2.], [3., 4.]], dtype=torch.float32)
    result = {"shape": list(values.shape), "dtype": str(values.dtype), "device": str(values.device),
              "sum": values.sum().item(), "matmul": (values @ values.T).tolist()}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
