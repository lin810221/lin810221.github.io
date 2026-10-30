"""Nearest-neighbor isolation in a small geometric dataset, not fraud detection."""
from embedding_core import nearest_neighbor_outlier_scores

if __name__ == "__main__":
    points = [[0., 0.], [.1, .2], [.2, .1], [5., 5.]]
    for index, score in enumerate(nearest_neighbor_outlier_scores(points)):
        print(index, points[index], "nearest-other distance:", round(score, 4))
