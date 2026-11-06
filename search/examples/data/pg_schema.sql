-- PostgreSQL 18.6 + pgvector extension 0.8.7. Use a disposable course database.
-- This is not automatically executed by any default Python example.
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS search_documents (
    point_id bigint PRIMARY KEY,
    tenant text NOT NULL,
    doc_id text NOT NULL,
    title text NOT NULL,
    body text NOT NULL,
    active boolean NOT NULL DEFAULT true,
    revision bigint NOT NULL CHECK (revision > 0),
    embedding vector(8) NOT NULL,
    search_text tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('simple', coalesce(title,'')), 'A') ||
        setweight(to_tsvector('simple', coalesce(body,'')), 'B')
    ) STORED,
    UNIQUE(tenant,doc_id)
);
CREATE INDEX IF NOT EXISTS search_text_gin ON search_documents USING gin(search_text);
CREATE INDEX IF NOT EXISTS search_scope ON search_documents(tenant,active);
CREATE INDEX IF NOT EXISTS search_cosine_hnsw ON search_documents USING hnsw(embedding vector_cosine_ops);
ALTER TABLE search_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE search_documents FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS tenant_isolation ON search_documents;
CREATE POLICY tenant_isolation ON search_documents
    USING (tenant = current_setting('app.tenant_id', true))
    WITH CHECK (tenant = current_setting('app.tenant_id', true));
-- Use a non-owner, non-superuser, non-BYPASSRLS application role.
-- app.tenant_id is set by a trusted transaction boundary, not by model SQL.
