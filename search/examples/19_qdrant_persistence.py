"""Close before reopening local storage; this is not a Qdrant server snapshot."""
from pathlib import Path
from tempfile import TemporaryDirectory
from qdrant_store import VectorStore
from search_core import fixtures

if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        path = Path(folder)/"vectors"
        with VectorStore(path) as store: store.upsert(fixtures()[0])
        with VectorStore(path) as restored:
            hits = restored.query("alpha","usb hub",1)
            assert hits[0].id == 1001
            print("reopened point",hits[0].id)
