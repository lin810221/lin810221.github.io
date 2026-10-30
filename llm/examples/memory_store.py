"""Application-managed user/thread isolation with parameterized SQLite queries."""
import json
import sqlite3


class MemoryStore:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS turns (owner TEXT, thread TEXT, seq INTEGER, text TEXT, PRIMARY KEY(owner,thread,seq))")
        self.db.execute("CREATE TABLE IF NOT EXISTS preferences (owner TEXT, key TEXT, value TEXT, PRIMARY KEY(owner,key))")
        self.db.commit()

    def append(self, owner: str, thread: str, text: str):
        # Serialize one writer transaction for sequence allocation.
        with self.db:
            self.db.execute("BEGIN IMMEDIATE")
            seq = self.db.execute("SELECT COALESCE(MAX(seq),0)+1 FROM turns WHERE owner=? AND thread=?", (owner,thread)).fetchone()[0]
            self.db.execute("INSERT INTO turns VALUES (?,?,?,?)", (owner,thread,seq,text))

    def history(self, owner: str, thread: str) -> list[str]:
        return [row[0] for row in self.db.execute("SELECT text FROM turns WHERE owner=? AND thread=? ORDER BY seq", (owner,thread))]

    def set_preference(self, owner: str, key: str, value):
        with self.db:
            self.db.execute("INSERT INTO preferences VALUES (?,?,?) ON CONFLICT(owner,key) DO UPDATE SET value=excluded.value", (owner,key,json.dumps(value)))

    def preference(self, owner: str, key: str):
        row = self.db.execute("SELECT value FROM preferences WHERE owner=? AND key=?", (owner,key)).fetchone()
        return json.loads(row[0]) if row else None

    def close(self):
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
