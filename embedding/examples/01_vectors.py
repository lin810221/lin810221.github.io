"""Handmade vectors illustrate arithmetic; no language model is run."""
from embedding_core import cosine, dot, euclidean, norm, unit

if __name__ == "__main__":
    query, a, b = [1., 0.], [2., 0.], [0., 1.]
    for label, values in [("A", a), ("B", b)]:
        print(label, {"norm": norm(values), "dot": dot(query, values), "cosine": cosine(query, values), "l2": euclidean(query, values)})
    print("normalized A:", unit(a))
