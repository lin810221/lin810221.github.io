"""Original positive-IDF BM25. Scores are not identical to SQLite's bm25()."""
from search_core import bm25

if __name__ == "__main__":
    corpus = {"short":"hub usb", "long":"hub "+"manual "*20, "repeat":"hub hub hub hub"}
    for k1,b in ((1.2,0.0),(1.2,0.75),(0.5,0.75)):
        print("k1",k1,"b",b,bm25(corpus,"hub",k1=k1,b=b))
