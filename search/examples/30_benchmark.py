"""Warm CPU index.search measurements, not cross-product capacity rankings."""
import json
from vector_indexes import sample,flat,hnsw,evaluate

if __name__ == "__main__":
    vectors,queries = sample(2048,32,24)
    exact,index = flat(vectors),hnsw(vectors)
    reports = []
    for ef in (8,32,128):
        index.hnsw.efSearch = ef
        reports.append({"ef_search":ef,**evaluate(index,exact,queries)})
    print(json.dumps(reports,indent=2))
