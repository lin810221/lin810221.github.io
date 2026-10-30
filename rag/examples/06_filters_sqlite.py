"""SQLite metadata storage plus permission-aware lexical retrieval; not ANN."""
import sqlite3
from rag_core import chunk_document, load_documents, read_store, retrieve, upsert_document

if __name__ == "__main__":
    with sqlite3.connect(":memory:") as connection:
        for doc in load_documents():
            upsert_document(connection, doc)
        chunks = [c for d in read_store(connection, "demo") for c in chunk_document(d)]
        for roles in ({"reader"}, {"hr"}, set()):
            hits = retrieve(chunks, "薪資設定", "demo", roles)
            print("roles:", sorted(roles), "visible hits:", [c.doc_id for c, _ in hits])
