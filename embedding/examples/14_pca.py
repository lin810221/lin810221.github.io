"""Actual analytic PCA from 2D to 1D, with centering and saved projection."""
from embedding_core import pca_2d

if __name__ == "__main__":
    result = pca_2d([[1., 1.], [2., 2.], [3., 3.], [4., 4.]])
    for key, value in result.items():
        print(key, value)
    print("This 1D example does not implement t-SNE or UMAP.")
