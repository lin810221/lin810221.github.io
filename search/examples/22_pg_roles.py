"""Identifiers need quoting; RLS also needs a real non-bypass application role."""
from pathlib import Path
from psycopg import sql

if __name__ == "__main__":
    statement = sql.SQL("SELECT doc_id FROM {} WHERE tenant=%s LIMIT %s").format(sql.Identifier("search_documents"))
    print(statement.as_string())
    schema = (Path(__file__).with_name("data")/"pg_schema.sql").read_text(encoding="utf-8")
    print(schema[schema.index("ALTER TABLE"):])
    print("Owner/superuser/BYPASSRLS and a user-controlled tenant GUC can defeat naive RLS assumptions.")
