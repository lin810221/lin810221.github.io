"""Round-trip a trusted local full-pipeline artifact, not just coefficients."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from pathlib import Path
import tempfile
from course_core import experiment,save_artifact,load_artifact,predict_records,sample_records

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        run=experiment()
        before=predict_records(run['artifact'],sample_records())
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'model.joblib'
            save_artifact(path,run['artifact'])
            restored=load_artifact(path)
            after=predict_records(restored,sample_records())
        result={'before':before,'after':after,'maximum_score_difference':
                float(np.max(np.abs(np.array(before['scores'])-np.array(after['scores'])))),
                'note':'joblib can execute code when loading; load only artifacts you trust'}
    return emit(result)

if __name__ == "__main__":
    main()
