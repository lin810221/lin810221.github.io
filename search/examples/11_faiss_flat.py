"""Real Faiss exact inner-product index over normalized float32 arrays."""
from vector_indexes import sample,flat,evaluate

if __name__ == "__main__":
    vectors,queries = sample()
    index = flat(vectors)
    report = evaluate(index,index,queries)
    assert report["recall_mean"] == 1
    print(report)
    print("Faiss IDs here are row positions; preserve an external stable-ID map.")
