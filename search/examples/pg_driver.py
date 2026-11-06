"""Optional live SELECT against an existing PostgreSQL/pgvector course table."""
import os
import numpy as np
import psycopg
from pgvector.psycopg import register_vector
from engine_clients import PG_QUERY, pg_parameters


def query_existing(tenant,text,k=5):
    dsn = os.environ.get("SEARCH_PG_DSN")
    if not dsn: raise ValueError("Set SEARCH_PG_DSN for your disposable, already initialized course database")
    with psycopg.connect(dsn,connect_timeout=5) as conn:
        conn.read_only = True
        register_vector(conn)
        conn.execute("SELECT set_config('app.tenant_id',%s,true)",(tenant,))
        query,scope,repeated,limit = pg_parameters(tenant,text,k)
        return conn.execute(PG_QUERY,(np.asarray(query,dtype="float32"),scope,
                                     np.asarray(repeated,dtype="float32"),limit)).fetchall()
