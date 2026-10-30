"""Hand-verifiable binary metrics and thresholds."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from course_core import binary_metrics

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        y=np.array([1,1,0,0])
        scores=np.array([.9,.4,.8,.1])
        result={'at_0_5':binary_metrics(y,scores,.5),'at_0_85':binary_metrics(y,scores,.85),
                'note':'fixed handmade scores, not model accuracy'}
    return emit(result)

if __name__ == "__main__":
    main()
