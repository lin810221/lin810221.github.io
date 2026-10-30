"""Small, transparent RAG building blocks. Python 3.11+, standard library only.

Lexical retrieval and extractive answers are real local algorithms; no pretrained
semantic encoder or generative LLM is simulated here. All documents are fictional.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
import re
import sqlite3
import unicodedata


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    text: str
    tenant: str = "demo"
    roles: tuple[str, ...] = ("reader",)
    version: str = "1"
    source: str = "demo://handbook"
    page: int = 1
    active: bool = True


@dataclass(frozen=True)
class Chunk:
    id: str
    doc_id: str
    title: str
    text: str
    tenant: str
    roles: tuple[str, ...]
    version: str
    source: str
    page: int
    start: int
    end: int
    active: bool


def normalize(text: str) -> str:
    """Offsets refer to THIS normalized text, not PDF byte offsets."""
    return unicodedata.normalize("NFC", text).replace("\r\n", "\n").replace("\r", "\n").strip()


def load_documents() -> list[Document]:
    path = Path(__file__).parent / "data" / "documents.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    return [Document(**{**row, "roles": tuple(row.get("roles", ["reader"]))}) for row in rows]


def tokenize(text: str) -> list[str]:
    """ASCII words/IDs + CJK characters/bigrams, NOT a model's token counter."""
    result = []
    for match in re.finditer(r"[a-zA-Z0-9]+(?:[-_][a-zA-Z0-9]+)*|[\u3400-\u9fff]+", normalize(text).lower()):
        word = match.group()
        if re.fullmatch(r"[\u3400-\u9fff]+", word):
            result.extend(word)
            result.extend(word[i:i + 2] for i in range(len(word) - 1))
        else:
            result.append(word)
    return result


def chunk_document(doc: Document, size: int = 180, overlap: int = 30) -> list[Chunk]:
    if not isinstance(size, int) or not isinstance(overlap, int) or size <= 0 or not 0 <= overlap < size:
        raise ValueError("Require integer size > 0 and 0 <= overlap < size")
    text = normalize(doc.text)
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        seed = json.dumps([doc.tenant, doc.id, doc.version, start, end, text[start:end]], ensure_ascii=False)
        identity = hashlib.sha256(seed.encode()).hexdigest()[:20]
        chunks.append(Chunk(identity, doc.id, doc.title, text[start:end], doc.tenant,
                            doc.roles, doc.version, doc.source, doc.page, start, end, doc.active))
        if end == len(text):
            break
        start = end - overlap
    return chunks


def visible(chunks: list[Chunk], tenant: str, roles: set[str]) -> list[Chunk]:
    if not tenant or not roles:
        return []
    return [chunk for chunk in chunks if chunk.active and chunk.tenant == tenant and set(chunk.roles) & roles]


class BM25:
    """BM25 with log(1 + (N - df + .5)/(df + .5)) positive IDF variant."""
    def __init__(self, chunks: list[Chunk], k1: float = 1.2, b: float = 0.75):
        if not math.isfinite(k1) or k1 <= 0 or not math.isfinite(b) or not 0 <= b <= 1:
            raise ValueError("Require k1 > 0 and 0 <= b <= 1")
        self.chunks, self.k1, self.b = chunks, k1, b
        self.counts = [Counter(tokenize(chunk.text)) for chunk in chunks]
        self.lengths = [sum(counts.values()) for counts in self.counts]
        self.average = sum(self.lengths) / len(chunks) if chunks else 0
        self.df = Counter(term for counts in self.counts for term in counts)

    def search(self, query: str, k: int = 5) -> list[tuple[Chunk, float]]:
        if k <= 0 or not self.average:
            return []
        terms = set(tokenize(query))
        n = len(self.chunks)
        scored = []
        for chunk, counts, length in zip(self.chunks, self.counts, self.lengths):
            score = 0.0
            for term in terms:
                frequency = counts[term]
                if not frequency:
                    continue
                df = self.df[term]
                idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
                denominator = frequency + self.k1 * (1 - self.b + self.b * length / self.average)
                score += idf * frequency * (self.k1 + 1) / denominator
            if score > 0:
                scored.append((chunk, score))
        return sorted(scored, key=lambda item: (-item[1], item[0].id))[:k]


def retrieve(chunks: list[Chunk], query: str, tenant: str = "demo", roles: set[str] | None = None,
             k: int = 5) -> list[tuple[Chunk, float]]:
    # Fit term statistics only on the caller's visible subset in this small demo.
    allowed = visible(chunks, tenant, {"reader"} if roles is None else roles)
    return BM25(allowed).search(query, k)


def cosine(left: list[float], right: list[float]) -> float:
    if not left or len(left) != len(right):
        raise ValueError("Vectors need equal nonzero dimensions")
    if not all(math.isfinite(x) for x in left + right):
        raise ValueError("Nonfinite vector")
    norm = math.hypot(*left) * math.hypot(*right)
    return sum(a * b for a, b in zip(left, right)) / norm if norm else 0.0


def rrf(rankings: list[list[tuple[Chunk, float]]], c: float = 60) -> list[tuple[Chunk, float]]:
    if not math.isfinite(c) or c <= 0:
        raise ValueError("RRF c must be positive")
    totals, chunks = Counter(), {}
    for ranking in rankings:
        seen = set()
        for rank, (chunk, _) in enumerate(ranking, 1):
            if chunk.id not in seen:
                totals[chunk.id] += 1 / (c + rank)
                chunks[chunk.id] = chunk
                seen.add(chunk.id)
    return sorted(((chunks[key], score) for key, score in totals.items()), key=lambda row: (-row[1], row[0].id))


def lexical_rerank(query: str, hits: list[tuple[Chunk, float]]) -> list[tuple[Chunk, float]]:
    """Explainable token-coverage reranker. NOT a neural cross-encoder."""
    terms = set(tokenize(query))
    if not terms:
        return []
    rows = [(chunk, len(terms & set(tokenize(chunk.text))) / len(terms)) for chunk, _ in hits]
    return sorted(rows, key=lambda row: (-row[1], row[0].id))


def pack_context(hits: list[tuple[Chunk, float]], budget_chars: int = 1000) -> tuple[str, dict[str, Chunk]]:
    """Exact CHARACTER budget incl labels. Token budgets need a model tokenizer."""
    if budget_chars < 0:
        raise ValueError("Negative budget")
    parts, evidence = [], {}
    used = 0
    seen = set()
    for chunk, _ in hits:
        # Identical content is redundant, but never dedup BEFORE authorization.
        if chunk.text in seen:
            continue
        label = f"S{len(parts) + 1}"
        block = f"[{label}] {chunk.title} | v{chunk.version} | p{chunk.page}\n{chunk.text}"
        cost = len(block) + (2 if parts else 0)
        if used + cost > budget_chars:
            continue  # Preserve whole chunks; a later small chunk may still fit.
        parts.append(block)
        evidence[label] = chunk
        seen.add(chunk.text)
        used += cost
    return "\n\n".join(parts), evidence


def extractive_answer(query: str, evidence: dict[str, Chunk]) -> dict:
    """Copies source sentences; coverage is a teaching heuristic, not entailment."""
    terms = set(tokenize(query))
    if not terms or not evidence:
        return {"status": "insufficient_evidence", "answer": "資料不足，請補充或改寫問題。", "citations": []}
    candidates = []
    for label, chunk in evidence.items():
        for sentence in re.split(r"(?<=[。！？.!?])\s*|\n+", chunk.text):
            overlap = len(terms & set(tokenize(sentence))) / len(terms)
            if sentence.strip():
                candidates.append((overlap, label, sentence.strip(), chunk))
    candidates.sort(key=lambda row: (-row[0], row[1], row[2]))
    if not candidates or candidates[0][0] < 0.35:
        return {"status": "insufficient_evidence", "answer": "資料不足，請補充或改寫問題。", "citations": []}
    _, label, sentence, chunk = candidates[0]
    return {"status": "extractive_demo", "answer": sentence + f" [{label}]",
            "citations": [{"label": label, "chunk_id": chunk.id, "doc_id": chunk.doc_id,
                           "source": chunk.source, "version": chunk.version, "page": chunk.page, "quote": sentence}]}


def validate_citations(answer: str, evidence: dict[str, Chunk]) -> bool:
    labels = re.findall(r"\[S\d+\]", answer)
    # This checks that referenced IDs exist, NOT whether the claim is entailed.
    return bool(labels) and all(label[1:-1] in evidence for label in labels)


def retrieval_metrics(ranked: list[str], relevant: dict[str, int], k: int = 5) -> dict:
    if k <= 0 or any(grade < 0 for grade in relevant.values()):
        raise ValueError("Require k > 0 and nonnegative relevance grades")
    # Repeated IDs get no additional gain, but occupy their actual rank position.
    seen, gains = set(), []
    for key in ranked[:k]:
        gains.append(relevant.get(key, 0) if key not in seen else 0)
        seen.add(key)
    total = sum(grade > 0 for grade in relevant.values())
    count = sum(grade > 0 for grade in gains)
    reciprocal = next((1 / index for index, grade in enumerate(gains, 1) if grade > 0), 0.0)
    dcg = sum((2 ** grade - 1) / math.log2(index + 1) for index, grade in enumerate(gains, 1))
    ideal = sorted(relevant.values(), reverse=True)[:k]
    idcg = sum((2 ** grade - 1) / math.log2(index + 1) for index, grade in enumerate(ideal, 1))
    return {"precision": count / k, "recall": count / total if total else 0.0,
            "mrr": reciprocal, "ndcg": dcg / idcg if idcg else 0.0}


def create_store(connection: sqlite3.Connection) -> None:
    connection.execute("CREATE TABLE IF NOT EXISTS documents (tenant TEXT, id TEXT, version TEXT, digest TEXT, payload TEXT, PRIMARY KEY(tenant,id))")


def upsert_document(connection: sqlite3.Connection, doc: Document) -> bool:
    """Atomically replace the small document record; retrieval reads latest state."""
    create_store(connection)
    payload = json.dumps(asdict(doc), ensure_ascii=False, sort_keys=True)
    digest = hashlib.sha256(payload.encode()).hexdigest()
    old = connection.execute("SELECT digest FROM documents WHERE tenant=? AND id=?", (doc.tenant, doc.id)).fetchone()
    if old and old[0] == digest:
        return False
    with connection:
        connection.execute("INSERT INTO documents VALUES(?,?,?,?,?) ON CONFLICT(tenant,id) DO UPDATE SET version=excluded.version,digest=excluded.digest,payload=excluded.payload",
                           (doc.tenant, doc.id, doc.version, digest, payload))
    return True


def read_store(connection: sqlite3.Connection, tenant: str) -> list[Document]:
    create_store(connection)
    rows = connection.execute("SELECT payload FROM documents WHERE tenant=? ORDER BY id", (tenant,)).fetchall()
    result = []
    for (payload,) in rows:
        record = json.loads(payload)
        record["roles"] = tuple(record["roles"])
        result.append(Document(**record))
    return result


def cache_key(query: str, tenant: str, roles: set[str], corpus_version: str, model: str) -> str:
    scope = [normalize(query), tenant, sorted(roles), corpus_version, model]
    return hashlib.sha256(json.dumps(scope, ensure_ascii=False).encode()).hexdigest()


def all_chunks() -> list[Chunk]:
    return [chunk for doc in load_documents() for chunk in chunk_document(doc)]


def ask(query: str, tenant: str = "demo", roles: set[str] | None = None, budget_chars: int = 1000) -> dict:
    chunks = all_chunks()
    hits = retrieve(chunks, query, tenant, roles)
    ranked = lexical_rerank(query, hits)
    context, evidence = pack_context(ranked, budget_chars)
    return {**extractive_answer(query, evidence), "context": context,
            "retrieved_doc_ids": [chunk.doc_id for chunk, _ in hits],
            "mode": "offline_bm25_extractive"}
