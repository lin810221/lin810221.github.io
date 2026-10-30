"""Token coverage heuristic, explicitly not a cross-encoder."""
from rag_core import all_chunks, lexical_rerank, retrieve

if __name__ == "__main__":
    query = "國內出差住宿費上限"
    hits = retrieve(all_chunks(), query)
    print("retrieval:", [(c.doc_id, round(s, 3)) for c, s in hits])
    print("coverage:", [(c.doc_id, round(s, 3)) for c, s in lexical_rerank(query, hits)])
