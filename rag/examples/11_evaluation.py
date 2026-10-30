"""Tiny synthetic development set, not evidence of production accuracy."""
import json
from pathlib import Path
from rag_core import all_chunks, retrieval_metrics, retrieve

if __name__ == "__main__":
    rows = json.loads((Path(__file__).parent / "data/qrels.json").read_text(encoding="utf-8"))
    scores = []
    for row in rows:
        # Evaluate at DOCUMENT level; overlapping chunks must not count twice.
        ids = list(dict.fromkeys(c.doc_id for c, _ in retrieve(all_chunks(), row["query"])))
        metrics = retrieval_metrics(ids, row["relevant"], k=3)
        scores.append(metrics)
        print(row["query"], metrics)
    print("macro average:", {name: sum(s[name] for s in scores) / len(scores) for name in scores[0]})
