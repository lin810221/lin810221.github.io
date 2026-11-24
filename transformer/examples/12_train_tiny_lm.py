"""Original offline teaching experiment; keep lm_core.py with this file."""
import argparse
from pathlib import Path
from lm_core import train_tiny,save_artifact,generate,ByteTokenizer,print_json
import torch

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args()
    model,report=train_tiny()
    ids=torch.tensor([ByteTokenizer().encode('red bird ',eos=False)])
    result=generate(model,ids,max_new_tokens=12)
    report['generated_ids']=result[0].tolist()
    report['generated_text']=ByteTokenizer().decode(result[0].tolist(),errors='replace')
    if args.output:save_artifact(model,args.output,report)
    print_json({k:v for k,v in report.items() if k!='history'})

if __name__=='__main__':main()
