"""Tiny self-authored development set; no production accuracy claim."""
from embedding_core import retrieval_metrics, workbench

if __name__ == "__main__":
    for query, relevant in [("向量 相似度", {"vectors"}), ("HTML 網頁結構", {"html"}), ("SQL 資料庫", {"database"})]:
        ranked = [row["id"] for row in workbench(query)["hits"]]
        print(query, retrieval_metrics(ranked, relevant, 3))
