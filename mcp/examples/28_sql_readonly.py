"""Use a fixed parameterized SELECT and an actual read-only SQLite connection."""
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory
import sqlite3


def query_status(path: Path, tenant: str, status: str) -> list[tuple]:
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as conn:
        return conn.execute("SELECT id,status FROM tickets WHERE tenant=? AND status=? LIMIT 10",
                            (tenant, status)).fetchall()


if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        path = Path(folder) / "fixture.sqlite"
        with closing(sqlite3.connect(path)) as conn:
            conn.execute("CREATE TABLE tickets(tenant TEXT,id TEXT,status TEXT)")
            conn.execute("INSERT INTO tickets VALUES ('alpha','T1','open')")
            conn.commit()
        print(query_status(path, "alpha", "open"))
        assert query_status(path, "alpha", "open' OR 1=1 --") == []
        print("SQL syntax in user data remains data")
