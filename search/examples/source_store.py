"""SQLite FTS5 source of truth, monotonic revisions and transactional outbox."""
from contextlib import closing
from dataclasses import asdict, replace
from pathlib import Path
import json
import apsw
from search_core import Document, tokenize


class SourceStore:
    def __init__(self, path=":memory:"):
        self.conn = apsw.Connection(str(path))
        self.conn.set_row_trace(lambda cursor, values: NamedRow(cursor.get_description(), values))
        self.conn.execute("""
          CREATE TABLE IF NOT EXISTS docs(
            rowid INTEGER PRIMARY KEY, point_id INTEGER NOT NULL UNIQUE,
            tenant TEXT NOT NULL, doc_id TEXT NOT NULL, title TEXT NOT NULL, body TEXT NOT NULL,
            category TEXT NOT NULL, revision INTEGER NOT NULL, active INTEGER NOT NULL,
            UNIQUE(tenant,doc_id));
          CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(title,body,content='docs',content_rowid='rowid');
          CREATE TRIGGER IF NOT EXISTS docs_ai AFTER INSERT ON docs BEGIN
            INSERT INTO docs_fts(rowid,title,body) VALUES(new.rowid,new.title,new.body); END;
          CREATE TRIGGER IF NOT EXISTS docs_ad AFTER DELETE ON docs BEGIN
            INSERT INTO docs_fts(docs_fts,rowid,title,body) VALUES('delete',old.rowid,old.title,old.body); END;
          CREATE TRIGGER IF NOT EXISTS docs_au AFTER UPDATE ON docs BEGIN
            INSERT INTO docs_fts(docs_fts,rowid,title,body) VALUES('delete',old.rowid,old.title,old.body);
            INSERT INTO docs_fts(rowid,title,body) VALUES(new.rowid,new.title,new.body); END;
          CREATE TABLE IF NOT EXISTS outbox(seq INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT NOT NULL UNIQUE,payload TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS checkpoints(worker TEXT PRIMARY KEY,last_seq INTEGER NOT NULL);
        """)

    def __enter__(self): return self
    def __exit__(self, *args): self.close()
    def close(self): self.conn.close()

    @staticmethod
    def decode(row):
        fields = {key: row[key] for key in Document.__dataclass_fields__}
        fields["active"] = bool(fields["active"])
        return Document(**fields)

    def get(self, tenant, doc_id):
        row = self.conn.execute("SELECT * FROM docs WHERE tenant=? AND doc_id=?", (tenant,doc_id)).fetchone()
        return self.decode(row) if row else None

    def by_point(self, tenant, point_id):
        row = self.conn.execute("SELECT * FROM docs WHERE tenant=? AND point_id=?", (tenant,point_id)).fetchone()
        return self.decode(row) if row else None

    def upsert(self, document: Document):
        old = self.get(document.tenant, document.doc_id)
        if old and old.point_id != document.point_id:
            raise ValueError("A logical document must keep its stable point ID")
        if old and document.revision < old.revision:
            raise ValueError("Stale revision cannot overwrite current source")
        if old and document.revision == old.revision:
            if old == document: return False
            raise ValueError("Same revision cannot describe different content")
        values = asdict(document)
        # Source write, FTS trigger updates and outbox are one SQLite transaction.
        with self.conn:
            self.conn.execute("""INSERT INTO docs(point_id,tenant,doc_id,title,body,category,revision,active)
              VALUES(:point_id,:tenant,:doc_id,:title,:body,:category,:revision,:active)
              ON CONFLICT(tenant,doc_id) DO UPDATE SET title=excluded.title,body=excluded.body,
                category=excluded.category,revision=excluded.revision,active=excluded.active""", values)
            event_id = json.dumps([document.tenant,document.doc_id,document.revision], separators=(",", ":"))
            self.conn.execute("INSERT INTO outbox(event_id,payload) VALUES(?,?)", (event_id,json.dumps(values)))
        return True

    def tombstone(self, tenant, doc_id, revision):
        old = self.get(tenant, doc_id)
        if not old: raise LookupError("Unknown source document")
        return self.upsert(replace(old, active=False, revision=revision))

    def documents(self, tenant=None, active_only=False):
        sql, args = "SELECT * FROM docs WHERE 1=1", []
        if tenant is not None: sql += " AND tenant=?"; args.append(tenant)
        if active_only: sql += " AND active=1"
        return [self.decode(row) for row in self.conn.execute(sql+" ORDER BY point_id", args)]

    def search(self, tenant, query, k=5):
        if not isinstance(tenant, str) or not tenant or type(k) is not int or not 1 <= k <= 100:
            raise ValueError("Trusted tenant and bounded integer k required")
        tokens = tokenize(query)
        if not tokens: return []
        # Literal AND terms: untrusted input cannot inject FTS operators either.
        expression = " AND ".join('"'+token.replace('"','""')+'"' for token in tokens)
        rows = self.conn.execute("""SELECT d.*,bm25(docs_fts,2.0,1.0) AS lexical_rank
          FROM docs_fts JOIN docs d ON d.rowid=docs_fts.rowid
          WHERE docs_fts MATCH ? AND d.tenant=? AND d.active=1
          ORDER BY lexical_rank ASC,d.point_id ASC LIMIT ?""", (expression,tenant,k)).fetchall()
        return [(self.decode(row), -float(row["lexical_rank"])) for row in rows]

    def events(self, after=0):
        return [(row["seq"],Document(**json.loads(row["payload"]))) for row in
                self.conn.execute("SELECT * FROM outbox WHERE seq>? ORDER BY seq", (after,))]

    def checkpoint(self, worker="qdrant"):
        row = self.conn.execute("SELECT last_seq FROM checkpoints WHERE worker=?", (worker,)).fetchone()
        return row[0] if row else 0

    def acknowledge(self, seq, worker="qdrant"):
        with self.conn:
            self.conn.execute("INSERT INTO checkpoints VALUES(?,?) ON CONFLICT(worker) DO UPDATE SET last_seq=max(last_seq,excluded.last_seq)", (worker,seq))

    def backup(self, destination: Path):
        if destination.exists(): raise FileExistsError("Backup destination must be new")
        with closing(apsw.Connection(str(destination))) as target:
            with target.backup("main", self.conn, "main") as backup:
                while not backup.done: backup.step(100)


class NamedRow(tuple):
    """Keep positional SQL rows while exposing explicit column-name access."""
    def __new__(cls, description, values):
        row = super().__new__(cls, values)
        row.columns = {column[0]: index for index, column in enumerate(description)}
        return row

    def __getitem__(self, key):
        return super().__getitem__(self.columns[key] if isinstance(key, str) else key)
