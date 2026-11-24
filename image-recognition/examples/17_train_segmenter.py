"""Offline executable teaching example; run from this directory."""
import argparse
from pathlib import Path
import torch
from vision_core import train_segmenter,make_shapes,save_preview,print_json

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    model,report=train_segmenter()
    if args.output:
        x,_,target,_=make_shapes(16,seed=41)
        with torch.inference_mode():pred=model(x).argmax(1)
        save_preview(args.output,x,report,prediction=pred,target=target)
        torch.save(model.state_dict(),args.output/'segmenter.pt')
    print_json(dict(dataset='original synthetic foreground shapes',**report))

if __name__=='__main__': main()
