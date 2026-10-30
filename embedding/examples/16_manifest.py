"""Vector spaces need explicit versions; equal dimensionality is insufficient."""
from dataclasses import replace
import sqlite3
from embedding_core import EmbeddingSpec, cache_key, read_vector, save_vector

if __name__ == "__main__":
    spec = EmbeddingSpec("teaching", "handmade", "v1", 2, "query-v1", "document-v1")
    updated = replace(spec, revision="v2")
    with sqlite3.connect(":memory:") as connection:
        save_vector(connection, "doc-1", [1., 0.], spec)
        print("original space:", read_vector(connection, "doc-1", spec))
        print("new space:", read_vector(connection, "doc-1", updated))
        print("query/document keys differ:", cache_key("hello", spec, "query") != cache_key("hello", spec, "document"))
