"""Synthetic labeled scores illustrate a decision threshold, not model accuracy."""
from embedding_core import binary_metrics

if __name__ == "__main__":
    labels = [1, 1, 1, 0, 0, 0]
    scores = [.92, .83, .69, .79, .48, .2]
    for threshold in (.5, .7, .85):
        print(threshold, binary_metrics(labels, scores, threshold))
