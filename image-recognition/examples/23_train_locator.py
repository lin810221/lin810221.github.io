"""Offline executable teaching example; run from this directory."""
import argparse
from pathlib import Path
import torch
from torch import nn
from vision_core import make_shapes,seed_everything,box_iou,save_preview,print_json

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args();seed_everything()
    x,_,_,boxes=make_shapes(96)
    model=nn.Sequential(nn.Conv2d(3,6,3,padding=1),nn.ReLU(),nn.AvgPool2d(2),
        nn.Flatten(),nn.Linear(6*12*12,4),nn.Sigmoid())
    optimizer=torch.optim.AdamW(model.parameters(),lr=.008)
    target=boxes/24
    for _ in range(120):
        optimizer.zero_grad(set_to_none=True)
        loss=nn.functional.smooth_l1_loss(model(x),target)
        loss.backward();optimizer.step()
    vx,_,_,truth=make_shapes(32,seed=41)
    model.eval()
    with torch.inference_mode():pred=model(vx)*24
    # Ordered boundaries are enforced at the output contract.
    lo=torch.minimum(pred[:,:2],pred[:,2:]);hi=torch.maximum(pred[:,:2],pred[:,2:])
    pred=torch.cat((lo,hi.clamp(min=1e-6)),1)
    iou=box_iou(pred,truth).diag()
    report={'task':'one guaranteed object per image; not a general detector',
            'valid_mean_iou':float(iou.mean()),'valid_n':32,'steps':120}
    if args.output:
        save_preview(args.output,vx,report,boxes=pred,true_boxes=truth)
        torch.save(model.state_dict(),args.output/'locator.pt')
    print_json(report)

if __name__=='__main__': main()
