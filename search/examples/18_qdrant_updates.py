"""Raw upsert is replacement, not application revision conflict control."""
from dataclasses import replace
from qdrant_store import VectorStore
from search_core import fixtures

if __name__ == "__main__":
    doc = fixtures()[0]
    with VectorStore() as store:
        store.upsert(doc)
        store.upsert(replace(doc,revision=2,title="USB hub revised"))
        point = store.query("alpha","usb hub",1)[0]
        assert point.payload["revision"] == 2
        store.delete(doc.point_id)
        assert store.query("alpha","usb hub",1) == []
    print("The source/outbox layer separately rejects stale revision events.")
