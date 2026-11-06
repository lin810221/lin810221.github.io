"""Fuse ranks, not incomparable raw BM25 and cosine scores."""
from search_core import rrf

if __name__ == "__main__":
    lexical = [(1001,9.8),(1002,3.1),(1008,0.9)]
    dense = [(1008,0.99),(1001,0.97),(1004,0.91)]
    print(rrf([lexical,dense],constant=60))
    print("Lexical branch only",rrf([lexical,dense],weights=[1,0]))
