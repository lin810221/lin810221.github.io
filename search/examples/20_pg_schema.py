"""Print PostgreSQL 18/pgvector 0.8.7 lab SQL; never create a database by default."""
from pathlib import Path

if __name__ == "__main__":
    sql = (Path(__file__).with_name("data")/"pg_schema.sql").read_text(encoding="utf-8")
    assert "vector_cosine_ops" in sql and "ENABLE ROW LEVEL SECURITY" in sql
    print(sql)
    print("SQL is inspected only. Run it explicitly in a disposable configured database.")
