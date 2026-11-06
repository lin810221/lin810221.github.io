"""Source authority prevents deleted/stale vector hits from leaking into output."""
from catalog_project import ALPHA,CatalogSearch,build_demo
from qdrant_store import replay

if __name__ == "__main__":
    source,vectors = build_demo()
    try:
        service = CatalogSearch(source,vectors,ALPHA)
        print("initial",service.search("usb hub",3))
        source.tombstone("alpha","AX-100",2)
        during_lag = service.search("usb hub",3)
        assert all(hit["point_id"] != 1001 for hit in during_lag["hits"])
        print("during indexing lag",during_lag)
        replay(source,vectors)
        print("after catch-up",service.search("usb hub",3))
    finally:
        vectors.close(); source.close()
