"""A real SQLite FTS5 search, no server or model API."""
from source_store import SourceStore
from search_core import fixtures

if __name__ == "__main__":
    with SourceStore() as store:
        for doc in fixtures(): store.upsert(doc)
        for doc,score in store.search("alpha","usb hub"):
            print(doc.doc_id,doc.title,"higher-is-better score",round(score,6))
        assert all(doc.tenant == "alpha" and doc.active for doc,score in store.search("alpha","usb"))
