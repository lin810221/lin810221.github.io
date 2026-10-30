"""Idempotent updates and tenant-scoped deletion in an in-memory database."""
from dataclasses import replace
import sqlite3
from rag_core import load_documents, read_store, upsert_document

if __name__ == "__main__":
    with sqlite3.connect(":memory:") as connection:
        doc = load_documents()[0]
        print("insert:", upsert_document(connection, doc))
        print("unchanged:", upsert_document(connection, doc))
        updated = replace(doc, version="2026-11", text=doc.text + "\n新增修訂說明。")
        print("update:", upsert_document(connection, updated))
        print("current:", [(d.id, d.version) for d in read_store(connection, "demo")])
        with connection:
            connection.execute("DELETE FROM documents WHERE tenant=? AND id=?", (doc.tenant, doc.id))
        print("after delete:", read_store(connection, "demo"))
