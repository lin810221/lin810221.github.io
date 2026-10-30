"""DBSCAN discovers dense groups and marks isolated points as -1."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,_=make_blobs(n_samples=60,centers=[[-2,0],[2,0]],cluster_std=.2,random_state=7)
        x=np.vstack([x,[[10.,10.]]])
        labels=DBSCAN(eps=.6,min_samples=4).fit_predict(x)
        result={'clusters':len(set(labels)-{-1}),'noise_count':int((labels==-1).sum()),
                'isolated_point_label':labels[-1],
                'note':'noise is a density-based designation, not proof of a bad record'}
    return emit(result)

if __name__ == "__main__":
    main()
