"""Original, deterministic search teaching primitives. No model downloads."""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from math import log, log2
import json
import re
import unicodedata
import numpy as np

RECIPE = "fixture-8d-v1"
DIMENSION = 8


@dataclass(frozen=True)
class Document:
    point_id: int
    tenant: str
    doc_id: str
    title: str
    body: str
    category: str
    revision: int = 1
    active: bool = True

    def __post_init__(self):
        if type(self.point_id) is not int or not 0 <= self.point_id < 2**63:
            raise ValueError("Shared SQLite/Qdrant IDs use the nonnegative signed-64 subset")
        if type(self.revision) is not int or self.revision < 1 or type(self.active) is not bool:
            raise ValueError("Positive integer revision and boolean active are required")
        for field in (self.tenant, self.doc_id, self.title, self.body, self.category):
            if not isinstance(field, str) or not field.strip():
                raise ValueError("Document text and identifiers cannot be blank")


def fixtures() -> list[Document]:
    path = Path(__file__).with_name("data") / "catalog.json"
    docs = [Document(**item) for item in json.loads(path.read_text(encoding="utf-8"))]
    if len({d.point_id for d in docs}) != len(docs) or len({(d.tenant, d.doc_id) for d in docs}) != len(docs):
        raise ValueError("Fixture identifiers must be unique")
    return docs


def tokenize(text: str) -> list[str]:
    """Unicode words; Han runs are not linguistically segmented."""
    return re.findall(r"[^\W_]+", unicodedata.normalize("NFKC", text).casefold(), re.UNICODE)


def han_bigrams(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    words = re.findall(r"[a-z0-9]+", normalized)
    for run in re.findall(r"[\u3400-\u9fff]+", normalized):
        words.extend([run] if len(run) == 1 else [run[i:i+2] for i in range(len(run)-1)])
    return words


def postings(corpus: dict[str, str]) -> dict:
    result = defaultdict(lambda: defaultdict(list))
    for doc_id, body in corpus.items():
        for position, token in enumerate(tokenize(body)):
            result[token][doc_id].append(position)
    return {term: dict(documents) for term, documents in sorted(result.items())}


def bm25(corpus: dict[str, str], query: str, *, k1=1.2, b=0.75) -> list[tuple[str, float]]:
    if not np.isfinite(k1) or k1 <= 0 or not np.isfinite(b) or not 0 <= b <= 1:
        raise ValueError("k1 must be positive and b must be within [0,1]")
    if not corpus:
        return []
    tokens = {key: tokenize(value) for key, value in corpus.items()}
    avgdl = sum(map(len, tokens.values())) / len(tokens)
    if avgdl == 0:
        return [(key, 0.0) for key in sorted(corpus)]
    query_terms = set(tokenize(query))
    scores = []
    for doc_id, values in tokens.items():
        tf, score = Counter(values), 0.0
        for term in query_terms:
            df = sum(term in body for body in tokens.values())
            idf = log(1 + (len(tokens) - df + 0.5) / (df + 0.5))
            denominator = tf[term] + k1 * (1 - b + b * len(values) / avgdl)
            if tf[term]:
                score += idf * tf[term] * (k1 + 1) / denominator
        scores.append((doc_id, score))
    return sorted(scores, key=lambda item: (-item[1], item[0]))


def matrix(values, dimension=None) -> np.ndarray:
    value = np.ascontiguousarray(values, dtype="float32")
    if value.ndim != 2 or not np.isfinite(value).all() or (dimension is not None and value.shape[1] != dimension):
        raise ValueError("A finite float32 matrix of the declared dimension is required")
    return value


def normalize(values) -> np.ndarray:
    values = matrix(values)
    norms = np.linalg.norm(values, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("A zero vector has no cosine direction")
    return np.ascontiguousarray(values / norms, dtype="float32")


def fixture_vector(text: str) -> list[float]:
    """Handcrafted 8-D features, NOT a learned semantic embedding model."""
    tokens = set(tokenize(text))
    groups = [set(x.split()) for x in ["hub dock ethernet adapter", "cable charging power",
        "battery repair lithium notebook", "vector hnsw filtering", "sql postgresql database",
        "backup replication operations", "搜尋 索引 中文 斷詞 查詢 bm25"]]
    raw = [float(len(tokens & group)) for group in groups] + [0.2]
    return normalize([raw])[0].tolist()


def exact_topk(vectors, query, k=5, eligible=None, metric="cosine") -> list[tuple[int, float]]:
    if type(k) is not int or k < 1:
        raise ValueError("k must be a positive integer")
    values = matrix(vectors)
    q = matrix([query], values.shape[1])[0]
    if metric == "cosine":
        scores = normalize(values) @ normalize([q])[0]
    elif metric == "dot":
        scores = values @ q
    elif metric == "l2":
        scores = -np.sum((values - q)**2, axis=1)
    else:
        raise ValueError("Unknown metric")
    indices = list(range(len(values))) if eligible is None else list(eligible)
    if any(type(i) is not int or not 0 <= i < len(values) for i in indices):
        raise ValueError("Invalid eligible ID")
    return sorted([(i, float(scores[i])) for i in set(indices)], key=lambda x: (-x[1], x[0]))[:k]


def rrf(rankings, *, constant=60.0, weights=None):
    weights = [1.0] * len(rankings) if weights is None else list(weights)
    if not np.isfinite(constant) or constant <= 0 or len(weights) != len(rankings):
        raise ValueError("Valid RRF constant and branch weights are required")
    if any(not np.isfinite(w) or w < 0 for w in weights) or not any(w > 0 for w in weights):
        raise ValueError("Weights must be nonnegative and at least one must be positive")
    scores = defaultdict(float)
    for ranking, weight in zip(rankings, weights):
        if weight == 0: continue
        seen = set()
        for rank, (doc_id, _) in enumerate(ranking, start=1):
            if doc_id in seen:
                raise ValueError("Duplicate ID inside a ranking")
            seen.add(doc_id)
            scores[doc_id] += weight / (constant + rank)
    return sorted(scores.items(), key=lambda x: (-x[1], str(x[0])))


def linear_fusion(rankings, weights):
    if len(rankings) != len(weights) or any(not np.isfinite(w) or w < 0 for w in weights) or sum(weights) <= 0:
        raise ValueError("Valid branch weights are required")
    totals = defaultdict(float)
    for rows, weight in zip(rankings, weights):
        if not rows or weight == 0:
            continue
        values = [score for _, score in rows]
        if not np.isfinite(values).all() or len({key for key, _ in rows}) != len(rows):
            raise ValueError("Finite scores with unique IDs are required")
        low, high = min(values), max(values)
        for doc_id, score in rows:
            totals[doc_id] += weight * ((score-low)/(high-low) if high > low else 0.0)
    return sorted(totals.items(), key=lambda x: (-x[1], str(x[0])))


def ann_recall(exact_ids, found_ids, k):
    if type(k) is not int or k < 1:
        raise ValueError("Positive k required")
    truth = set(list(exact_ids)[:k])
    return len(truth & set(list(found_ids)[:k])) / len(truth) if truth else None


def ndcg(ranking, qrels, k=5):
    if len(set(ranking)) != len(ranking) or type(k) is not int or k < 1:
        raise ValueError("Unique ranked IDs and positive k required")
    if any(not np.isfinite(value) or value < 0 for value in qrels.values()):
        raise ValueError("Nonnegative finite relevance grades required")
    gain = lambda values: sum((2**grade-1)/log2(rank+2) for rank, grade in enumerate(values))
    ideal = gain(sorted(qrels.values(), reverse=True)[:k])
    actual = gain([qrels.get(key, 0) for key in ranking[:k]])
    return actual / ideal if ideal else None


def capacity(n, dimension, *, bits=32, neighbors=16, replicas=1, headroom=1.3, keep_original=False):
    if any(type(value) is not int or value < 1 for value in (n, dimension, bits, neighbors, replicas)) or not np.isfinite(headroom) or headroom < 1:
        raise ValueError("Positive capacity inputs and headroom >=1 required")
    # Approximation only: excludes metadata, upper graph levels, allocators, WAL,
    # caches and disk structures. Replicas here means total stored copies.
    vectors = n * dimension * bits / 8
    originals = n * dimension * 4 if keep_original and bits != 32 else 0
    graph = n * neighbors * 2 * 4
    total = (vectors + originals + graph) * replicas * headroom
    return {"vectors": vectors, "retained_originals": originals, "graph_approx": graph,
            "estimated_bytes": total, "GB": total/1e9, "GiB": total/2**30}
