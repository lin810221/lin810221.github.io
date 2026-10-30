"""Actual save/load and raw-feature prediction from an independent complete artifact."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from pathlib import Path
import argparse,tempfile
from course_core import experiment,prediction_rows,predict_tabular,save_artifact,load_artifact

def main(argv=None):
    setup()
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path)
    args=parser.parse_args(argv)
    if args.output and args.output.exists():parser.error('Choose a new output filename')
    run=experiment('tabular');payload=run['artifact'];rows=prediction_rows()
    before=predict_tabular(payload,rows)
    if args.output:
        save_artifact(args.output,payload);loaded=load_artifact(args.output);saved=str(args.output)
    else:
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'model.pt';save_artifact(path,payload);loaded=load_artifact(path)
        saved='temporary directory, removed after demonstration'
    after=predict_tabular(loaded,rows)
    result={'torch':loaded['torch_version'],'initial_validation':run['initial_validation'],
            'best_validation':run['best_validation'],'test':run['test'],'predictions':after,
            'maximum_roundtrip_error':max(abs(a-b) for left,right in zip(before['probabilities'],after['probabilities']) for a,b in zip(left,right)),
            'saved_to':saved,'scope':'inference artifact; not an exact-resume checkpoint'}
    return emit(result)

if __name__=="__main__":
    main()
