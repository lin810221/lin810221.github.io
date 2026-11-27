"""Persist a synthetic CDC batch and publish a recoverable local Parquet snapshot."""
from pathlib import Path
import argparse,json
from pipeline import process_batch,read_current

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace',required=True,type=Path)
    parser.add_argument('--batch',type=Path)
    parser.add_argument('--show',action='store_true')
    parser.add_argument('--fault',choices=['before_commit','after_commit','after_pointer'])
    args=parser.parse_args()
    if not args.batch and not args.show:parser.error('Choose --batch or --show')
    if args.batch:
        batch=json.loads(args.batch.read_text(encoding='utf-8'))
        print(json.dumps(process_batch(args.workspace,batch,args.fault),ensure_ascii=False))
    if args.show:print(json.dumps(read_current(args.workspace),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
