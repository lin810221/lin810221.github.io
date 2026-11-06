"""Same revision is idempotent only when its content is also identical."""
from dataclasses import replace
from search_core import fixtures
from source_store import SourceStore

if __name__ == "__main__":
    original = fixtures()[0]
    with SourceStore() as store:
        assert store.upsert(original)
        assert not store.upsert(original)
        assert store.upsert(replace(original,revision=2,title="Revised USB hub"))
        try: store.upsert(original)
        except ValueError: print("stale source write rejected")
        print("outbox events",len(store.events()))
