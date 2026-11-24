"""Offline executable teaching example; run from this directory."""
import argparse
from pathlib import Path
import torch
from vision_core import train_classifier,make_shapes,save_preview,artifact_contract,print_json

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    model,report=train_classifier()
    if args.output:
        x,y,_,_=make_shapes(16,seed=41)
        with torch.inference_mode():pred=model(x).argmax(1)
        report['preview_labels']={'true':y[:8].tolist(),'pred':pred[:8].tolist()}
        save_preview(args.output,x,report)
        path=args.output/'classifier.pt';torch.save(model.state_dict(),path)
        import json
        (args.output/'contract.json').write_text(json.dumps(artifact_contract(path),indent=2),encoding='utf-8')
    print_json(dict(dataset='original synthetic squares vs bars',**report))

if __name__=='__main__': main()
