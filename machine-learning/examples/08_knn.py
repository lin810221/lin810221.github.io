"""Scaled distance and k-neighbor classification."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from course_core import binary_data,holdout,probability,binary_metrics

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        x,y=binary_data()
        a,b,c,d=holdout(x,y)
        model=make_pipeline(StandardScaler(),KNeighborsClassifier(n_neighbors=7,weights='distance')).fit(a,c)
        distance,index=model[-1].kneighbors(model[0].transform(b[:1]))
        result={'first_query_neighbors':index,'scaled_distances':distance,
                'holdout':binary_metrics(d,probability(model,b))}
    return emit(result)

if __name__ == "__main__":
    main()
