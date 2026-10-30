"""Default FP32 CPU path; --cuda-amp explicitly requires an available CUDA GPU."""
import argparse
import json
import torch
from torch import nn
from course_core import amp_step, choose_device, setup

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cuda-amp", action="store_true")
    args = parser.parse_args(argv)
    setup()
    device = choose_device("cuda" if args.cuda_amp else "cpu")
    model = nn.Linear(4,3).to(device)
    optimizer = torch.optim.SGD(model.parameters(),lr=.1)
    x,y = torch.randn(8,4,device=device),torch.arange(8,device=device)%3
    result = amp_step(model,optimizer,x,y,args.cuda_amp)
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
