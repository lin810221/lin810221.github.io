"""Handmade vectors show geometry; they are NOT learned semantic embeddings."""
from rag_core import cosine

if __name__ == "__main__":
    query = [1.0, 0.0, 0.0]
    vectors = {"A": [0.9, 0.1, 0.0], "B": [0.0, 1.0, 0.0], "C": [-1.0, 0.0, 0.0]}
    for key, vector in sorted(vectors.items(), key=lambda pair: -cosine(query, pair[1])):
        print(key, round(cosine(query, vector), 4))
    print("A is closest geometrically; no semantic model was run.")
