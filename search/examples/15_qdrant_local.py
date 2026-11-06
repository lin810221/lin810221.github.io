"""Qdrant Local stores real named dense/sparse vectors, without a server."""
from qdrant_store import VectorStore
from search_core import fixtures

if __name__ == "__main__":
    with VectorStore() as store:
        for doc in fixtures(): store.upsert(doc)
        for point in store.query("alpha","usb hub",3): print(point.id,point.payload,point.score)
    print("Local query semantics tested; server HNSW/replication not exercised.")
