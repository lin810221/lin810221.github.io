"""Rank fusion on two literal query variants. No dense encoder is implied."""
from rag_core import all_chunks, retrieve, rrf

if __name__ == "__main__":
    chunks = all_chunks()
    rankings = [retrieve(chunks, query) for query in ["出差住宿", "差旅報銷"]]
    for chunk, score in rrf(rankings):
        print(round(score, 6), chunk.doc_id)
    print("A real hybrid system may fuse BM25 and dense retrieval in the same way.")
