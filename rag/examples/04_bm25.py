"""Fit term statistics after authorization, then rank visible chunks."""
from rag_core import BM25, all_chunks, tokenize, visible

if __name__ == "__main__":
    query = "VPN-403 授權"
    chunks = visible(all_chunks(), "demo", {"reader"})
    print("query terms:", tokenize(query))
    for chunk, score in BM25(chunks).search(query):
        print(round(score, 4), chunk.doc_id, chunk.text)
