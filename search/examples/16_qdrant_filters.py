"""Filter semantics work locally; payload index performance requires a server."""
from qdrant_client import models
from qdrant_store import VectorStore,tenant_filter
from search_core import fixtures

if __name__ == "__main__":
    with VectorStore() as store:
        for doc in fixtures(): store.upsert(doc)
        hits = store.query("alpha","vector index",5)
        assert all(p.payload["tenant"]=="alpha" and p.payload["active"] for p in hits)
        print("filter",tenant_filter("alpha").model_dump(exclude_none=True))
        print("server payload-index field type",models.PayloadSchemaType.KEYWORD.value)
    print("create_payload_index is intentionally not used as a local performance test.")
