"""Full mixed-table project: training CV, validation threshold, one final test."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from pathlib import Path
import argparse,tempfile
from course_core import Config,experiment,save_artifact,load_artifact,predict_records,sample_records

def main(argv=None):
    with threadpool_limits(limits=1):
        parser=argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--output',type=Path)
        args=parser.parse_args(argv)
        if args.output and args.output.exists():
            parser.error('Choose a new output filename')
        run=experiment(Config())
        if args.output:
            save_artifact(args.output,run['artifact'])
            restored=load_artifact(args.output)
            saved=str(args.output)
        else:
            with tempfile.TemporaryDirectory() as folder:
                path=Path(folder)/'model.joblib'
                save_artifact(path,run['artifact'])
                restored=load_artifact(path)
            saved='temporary directory, removed after demonstration'
        result={'versions':restored['versions'],'splits':run['split_sizes'],
                'training_selection':restored['selection'],'final_test':run['test'],
                'new_records':predict_records(restored,sample_records()),'saved_to':saved,
                'data':restored['data']}
    return emit(result)

if __name__ == "__main__":
    main()
