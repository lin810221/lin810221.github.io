"""A worker crash after the index write can safely replay the same event."""
from search_core import fixtures
from source_store import SourceStore
from qdrant_store import VectorStore,replay

if __name__ == "__main__":
    with SourceStore() as source, VectorStore() as vectors:
        source.upsert(fixtures()[0])
        try: replay(source,vectors,fail_after_write=True)
        except RuntimeError: print("worker stopped before checkpoint",source.checkpoint())
        replay(source,vectors)
        assert source.checkpoint() == 1
        assert vectors.client.count(vectors.collection,exact=True).count == 1
        print("one point after at-least-once replay")
