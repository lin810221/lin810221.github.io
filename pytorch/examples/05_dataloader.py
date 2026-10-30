"""Default workers=0; the main guard also supports Windows spawn."""
import argparse
import json
import torch
from torch.utils.data import DataLoader
from course_core import custom_dataset, seed_worker

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=0)
    args = parser.parse_args(argv)
    if args.workers < 0:
        parser.error("workers must be nonnegative")
    loader = DataLoader(custom_dataset(), batch_size=4, shuffle=True, num_workers=args.workers,
                        worker_init_fn=seed_worker, generator=torch.Generator().manual_seed(7))
    batches = [{"x": list(x.shape), "y": list(y.shape), "labels": y.tolist()} for x, y in loader]
    result = {"batches": batches, "samples": sum(batch["y"][0] for batch in batches)}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
