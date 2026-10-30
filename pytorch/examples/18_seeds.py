"""Separate torch.Generator streams help avoid accidental RNG coupling."""
import json
import torch

def main(argv=None):
    del argv
    first = torch.randperm(8, generator=torch.Generator().manual_seed(7))
    torch.rand(100)  # Unrelated global RNG activity does not alter the new local generator.
    second = torch.randperm(8, generator=torch.Generator().manual_seed(7))
    third = torch.randperm(8, generator=torch.Generator().manual_seed(8))
    result = {"same_seed_same_order": torch.equal(first,second),
              "different_seed_changes_order": not torch.equal(first,third), "order": first.tolist()}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
