"""Actual query_points/prefetch/FusionQuery with identical branch filters."""
from qdrant_store import VectorStore
from search_core import fixtures

if __name__ == "__main__":
    with VectorStore() as store:
        for doc in fixtures(): store.upsert(doc)
        hits = store.query("alpha","usb hub",3,hybrid=True)
        print([(p.id,round(p.score,6),p.payload["doc_id"]) for p in hits])
    print("Sparse branch uses fixture term frequencies, not a production BM25 model.")
