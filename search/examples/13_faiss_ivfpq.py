"""Train IVF-PQ, vary nprobe, and compare with the same exact baseline."""
from vector_indexes import sample,flat,ivfpq,evaluate

if __name__ == "__main__":
    vectors,queries = sample()
    exact = flat(vectors)
    index = ivfpq(vectors,nlist=16,subquantizers=4,bits=4)
    for nprobe in (1,4,16):
        index.nprobe = nprobe
        print("nprobe",nprobe,evaluate(index,exact,queries))
    print("Searching all coarse cells still leaves PQ approximation error.")
