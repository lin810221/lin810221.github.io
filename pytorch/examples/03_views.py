"""Contiguity, shared storage, reshape, detach and clone."""
import json
import torch

def main(argv=None):
    del argv
    x = torch.arange(6., dtype=torch.float32).reshape(2, 3)
    transposed = x.T
    try:
        transposed.view(-1)
        view_failed = False
    except RuntimeError:
        view_failed = True
    detached = x.detach()
    cloned = x.clone()
    detached[0, 0] = 99
    result = {"original_stride": list(x.stride()), "transpose_stride": list(transposed.stride()),
              "view_failed": view_failed, "reshape": transposed.reshape(-1).tolist(),
              "detach_changed_original": x[0, 0].item() == 99,
              "clone_unchanged": cloned[0, 0].item() == 0}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
