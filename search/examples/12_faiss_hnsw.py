"""A real CPU HNSW experiment, not a browser graph simulation."""
from vector_indexes import sample,flat,hnsw,evaluate

if __name__ == "__main__":
    vectors,queries = sample()
    exact = flat(vectors)
    index = hnsw(vectors,neighbors=16,construction=64)
    for ef in (8,32,128):
        index.hnsw.efSearch = ef
        print("efSearch",ef,evaluate(index,exact,queries))
    print("No universal monotonic latency or production recall guarantee.")
