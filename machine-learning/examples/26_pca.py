"""PCA projects, reconstructs and reports explained variance."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.decomposition import PCA

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        rng=np.random.default_rng(7)
        t=np.linspace(-2,2,80)
        x=np.column_stack([t,2*t+rng.normal(0,.05,len(t)),rng.normal(0,.02,len(t))])
        model=PCA(n_components=1,svd_solver='full').fit(x)
        projected=model.transform(x)
        reconstructed=model.inverse_transform(projected)
        result={'component':model.components_,'explained_variance_ratio':model.explained_variance_ratio_,
                'projected_shape':projected.shape,'reconstruction_mse':float(np.mean((x-reconstructed)**2)),
                'note':'PCA maximizes variance, not class separation; component sign is arbitrary'}
    return emit(result)

if __name__ == "__main__":
    main()
