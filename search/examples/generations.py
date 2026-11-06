"""A transactional application generation registry; not a distributed DB alias."""
import apsw


class IndexRegistry:
    def __init__(self,path=":memory:"):
        self.conn = apsw.Connection(str(path))
        self.conn.execute("""
          CREATE TABLE IF NOT EXISTS generations(name TEXT PRIMARY KEY,recipe TEXT NOT NULL,verified INTEGER NOT NULL);
          CREATE TABLE IF NOT EXISTS control(id INTEGER PRIMARY KEY CHECK(id=1),name TEXT,recipe TEXT);
          INSERT OR IGNORE INTO control VALUES(1,NULL,NULL);
        """)

    def close(self): self.conn.close()
    def __enter__(self): return self
    def __exit__(self,*args): self.close()

    def register(self,name,recipe):
        if not name or not recipe: raise ValueError("Generation and recipe are required")
        with self.conn: self.conn.execute("INSERT INTO generations VALUES(?,?,0)",(name,recipe))

    def verify(self,name,checks):
        required = {"contract","scope","quality","checkpoint"}
        if not required <= checks.keys() or not all(checks[key] is True for key in required):
            raise ValueError("All mandatory checks must have real passing evidence")
        with self.conn:
            self.conn.execute("UPDATE generations SET verified=1 WHERE name=?",(name,))
            if self.conn.changes() != 1:
                raise LookupError("Unknown generation")

    def current(self):
        name,recipe = self.conn.execute("SELECT name,recipe FROM control WHERE id=1").fetchone()
        return {"generation":name,"query_recipe":recipe}

    def activate(self,name,expected_current,query_recipe):
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            if self.current()["generation"] != expected_current:
                raise ValueError("Active generation changed; retry from current state")
            target = self.conn.execute("SELECT recipe,verified FROM generations WHERE name=?",(name,)).fetchone()
            if not target or not target[1] or target[0] != query_recipe:
                raise ValueError("A verified generation and matching query recipe are required")
            self.conn.execute("UPDATE control SET name=?,recipe=? WHERE id=1",(name,query_recipe))
            self.conn.execute("COMMIT")
        except BaseException:
            self.conn.execute("ROLLBACK")
            raise
        return self.current()
