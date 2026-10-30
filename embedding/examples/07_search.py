"""Exact search over real local TF-IDF vectors, not pretrained semantics."""
from embedding_core import workbench

if __name__ == "__main__":
    for row in workbench("向量 相似度 cosine")["hits"]:
        print(row["id"], round(row["score"], 4), row["text"])
