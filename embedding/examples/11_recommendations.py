"""Content-based lexical recommendations. Seen items are excluded explicitly."""
from embedding_core import Tfidf, load_data, search, unit

if __name__ == "__main__":
    rows = load_data()
    encoder = Tfidf().fit([row["text"] for row in rows])
    vectors = [encoder.transform(row["text"]) for row in rows]
    seen = {"vectors", "training"}
    history = [values for row, values in zip(rows, vectors) if row["id"] in seen]
    profile = unit([sum(v[j] for v in history) / len(history) for j in range(len(vectors[0]))])
    for index, score in search(profile, vectors, len(rows)):
        if rows[index]["id"] not in seen and score > 0:
            print(rows[index]["id"], round(score, 4))
