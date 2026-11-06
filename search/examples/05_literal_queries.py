"""Both SQL parameters and literal FTS terms are controlled."""
from source_store import SourceStore
from search_core import fixtures

if __name__ == "__main__":
    with SourceStore() as store:
        for doc in fixtures(): store.upsert(doc)
        for query in ("usb", "usb hub", "usb OR confidential", "\" OR 1=1 --"):
            hits = store.search("alpha",query)
            print(repr(query),[doc.doc_id for doc,score in hits])
            assert all(doc.tenant == "alpha" and doc.active for doc,score in hits)
        print("Advanced FTS operators need a separate trusted query interface.")
