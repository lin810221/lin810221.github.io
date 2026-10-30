"""Actual Euclidean K-means on handmade points, with silhouette calculation."""
from embedding_core import kmeans, silhouette

if __name__ == "__main__":
    points = [[0., 0.], [.2, .1], [0., .3], [4., 4.], [4.2, 4.1], [4., 4.3]]
    centers, labels, inertia = kmeans(points, 2)
    print("centers:", centers, "labels:", labels)
    print("inertia:", inertia, "silhouette:", silhouette(points, labels))
