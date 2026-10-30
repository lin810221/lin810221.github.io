"""Default prints a plan. --run requires torchrun and an environment supporting Gloo."""
import argparse
import json
import os
from datetime import timedelta
import torch
from torch import nn
from torch.nn import functional as F
from torch.nn.parallel import DistributedDataParallel
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.data.distributed import DistributedSampler
from course_core import setup

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run",action="store_true")
    args = parser.parse_args(argv)
    if not args.run:
        result = {"mode":"plan_only","command":"torchrun --standalone --nproc-per-node=2 23_distributed.py --run",
                  "scope":"CPU/Gloo, optional multi-process execution; default opens no ports"}
        print(json.dumps(result,indent=2))
        return result
    if "RANK" not in os.environ or "WORLD_SIZE" not in os.environ:
        parser.error("Launch --run with torchrun")
    import torch.distributed as dist
    if not dist.is_available() or not dist.is_gloo_available():
        raise RuntimeError("This build does not provide Gloo")
    setup()
    dist.init_process_group("gloo",timeout=timedelta(seconds=60))
    try:
        x,y = torch.randn(16,4),torch.arange(16)%3
        dataset = TensorDataset(x,y)
        sampler = DistributedSampler(dataset,shuffle=True,seed=7)
        loader = DataLoader(dataset,batch_size=4,sampler=sampler)
        model = DistributedDataParallel(nn.Linear(4,3))
        optimizer = torch.optim.SGD(model.parameters(),lr=.1)
        sampler.set_epoch(0)
        for batch,target in loader:
            optimizer.zero_grad(set_to_none=True)
            F.cross_entropy(model(batch),target).backward()
            optimizer.step()
        checksum = sum(parameter.detach().sum() for parameter in model.parameters())
        gathered = [torch.zeros_like(checksum) for _ in range(dist.get_world_size())]
        dist.all_gather(gathered,checksum)
        result = {"rank":dist.get_rank(),"checksums":[value.item() for value in gathered]}
        print(json.dumps(result,indent=2))
        return result
    finally:
        dist.destroy_process_group()

if __name__ == "__main__":
    main()
