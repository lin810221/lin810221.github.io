"""Nearest class centroid; fit only on the explicitly designated training rows."""
from embedding_core import Tfidf, centroids, classify

if __name__ == "__main__":
    training = [("向量 相似度 cosine", "ml"), ("模型 梯度 訓練", "ml"),
                ("網頁 HTML 表單", "web"), ("網頁 CSS 樣式", "web"),
                ("資料庫 SQL 交易", "systems"), ("服務 部署 監控", "systems")]
    encoder = Tfidf().fit([text for text, _ in training])
    prototypes = centroids([encoder.transform(text) for text, _ in training], [label for _, label in training])
    for query in ["向量 cosine", "網頁 表單", "SQL 交易"]:
        label, score = classify(encoder.transform(query), prototypes)
        print(query, "->", label, "cosine:", round(score, 4), "(not a calibrated probability)")
