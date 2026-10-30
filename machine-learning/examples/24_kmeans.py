"""KMeans minimizes within-cluster squared distance on synthetic blobs."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score,adjusted_rand_score

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,truth=make_blobs(n_samples=90,centers=[[-3,-2],[0,3],[3,-2]],cluster_std=.5,random_state=7)
        model=KMeans(n_clusters=3,n_init=10,random_state=7).fit(x)
        result={'centers':model.cluster_centers_,'inertia':model.inertia_,
                'silhouette':silhouette_score(x,model.labels_),
                'synthetic_truth_ari':adjusted_rand_score(truth,model.labels_),
                'note':'cluster IDs are arbitrary; truth is available only because this is generated data'}
    return emit(result)

if __name__ == "__main__":
    main()
