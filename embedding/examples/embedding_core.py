"""Transparent numerical teaching tools. Python 3.11+, no dependencies/network.

TF-IDF is lexical, handmade vectors show geometry, and tiny Skip-gram training
does NOT reproduce the quality of a pretrained semantic model.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
import random
import re
import sqlite3
import unicodedata


def vector(values, dimensions=None):
    result = [float(value) for value in values]
    if not result or (dimensions is not None and len(result) != dimensions):
        raise ValueError("Nonempty vector with matching dimensions required")
    if not all(math.isfinite(x) for x in result):
        raise ValueError("Vector must contain only finite numbers")
    return result


def dot(left, right):
    left = vector(left)
    right = vector(right, len(left))
    return math.fsum(a * b for a, b in zip(left, right))


def norm(values):
    return math.hypot(*vector(values))


def unit(values):
    values = vector(values)
    length = norm(values)
    if length == 0:
        raise ValueError("Zero vector has no direction")
    return [value / length for value in values]


def cosine(left, right):
    left = unit(left)
    right = unit(vector(right, len(left)))
    return max(-1.0, min(1.0, dot(left, right)))


def euclidean(left, right):
    left = vector(left)
    right = vector(right, len(left))
    return math.hypot(*(a - b for a, b in zip(left, right)))


def tokens(text):
    text = unicodedata.normalize("NFC", text).lower()
    result = []
    for term in re.findall(r"[a-z0-9]+(?:[-_][a-z0-9]+)*|[\u3400-\u9fff]+", text):
        if re.fullmatch(r"[\u3400-\u9fff]+", term):
            result.extend(term)
            result.extend(term[i:i + 2] for i in range(len(term) - 1))
        else:
            result.append(term)
    return result


class Tfidf:
    """Training-corpus vocabulary/IDF, raw TF and L2 normalization. Not semantic."""
    def fit(self, texts):
        texts = list(texts)
        if not texts:
            raise ValueError("Training texts required")
        counts = [Counter(tokens(text)) for text in texts]
        self.vocabulary = sorted({term for count in counts for term in count})
        if not self.vocabulary:
            raise ValueError("No supported tokens in training corpus")
        df = Counter(term for count in counts for term in count)
        self.idf = [math.log((1 + len(texts)) / (1 + df[term])) + 1 for term in self.vocabulary]
        return self

    def transform(self, text):
        if not hasattr(self, "vocabulary"):
            raise ValueError("Fit on the training corpus first")
        count = Counter(tokens(text))
        values = [count[term] * idf for term, idf in zip(self.vocabulary, self.idf)]
        length = math.hypot(*values)
        # Unknown-only query remains zero and retrieves nothing.
        return [value / length for value in values] if length else values


def search(query_vector, vectors, k=5):
    if k <= 0:
        return []
    query_vector = vector(query_vector)
    if norm(query_vector) == 0:
        return []
    rows = []
    for index, values in enumerate(vectors):
        values = vector(values, len(query_vector))
        if norm(values):
            rows.append((index, cosine(query_vector, values)))
    return sorted(rows, key=lambda item: (-item[1], item[0]))[:k]


def cooccurrence(words, window=1):
    if window < 1:
        raise ValueError("Positive context window required")
    vocabulary = sorted(set(words))
    positions = {word: i for i, word in enumerate(vocabulary)}
    matrix = [[0.0] * len(vocabulary) for _ in vocabulary]
    for index, word in enumerate(words):
        for context_index in range(max(0, index - window), min(len(words), index + window + 1)):
            if context_index != index:
                matrix[positions[word]][positions[words[context_index]]] += 1
    return vocabulary, matrix


def ppmi(matrix):
    if not matrix:
        return []
    width = len(matrix[0])
    if not width or any(len(row) != width or any(not math.isfinite(x) or x < 0 for x in row) for row in matrix):
        raise ValueError("Finite nonnegative rectangular matrix required")
    row_sums = [sum(row) for row in matrix]
    column_sums = [sum(row[j] for row in matrix) for j in range(width)]
    total = sum(row_sums)
    return [[max(0.0, math.log(value * total / (row_sums[i] * column_sums[j])))
             if value and row_sums[i] and column_sums[j] else 0.0
             for j, value in enumerate(row)] for i, row in enumerate(matrix)]


def sigmoid(value):
    if value >= 0:
        return 1 / (1 + math.exp(-value))
    exponential = math.exp(value)
    return exponential / (1 + exponential)


def binary_logit_loss(logit, label):
    if label not in (0, 1) or not math.isfinite(logit):
        raise ValueError("Binary label and finite logit required")
    return max(logit, 0) - label * logit + math.log1p(math.exp(-abs(logit)))


def skipgram_step(target, context, label, learning_rate=0.1):
    if not 0 < learning_rate <= 1:
        raise ValueError("Require 0 < learning_rate <= 1")
    old_target, old_context = vector(target), vector(context, len(target))
    logit = dot(old_target, old_context)
    loss = binary_logit_loss(logit, label)
    gradient = sigmoid(logit) - label
    for index in range(len(target)):
        target[index] = old_target[index] - learning_rate * gradient * old_context[index]
        context[index] = old_context[index] - learning_rate * gradient * old_target[index]
    return loss


def tiny_skipgram(epochs=120, seed=7):
    """Genuine tiny logistic vector training; fixed negatives, no language claims."""
    if epochs < 0:
        raise ValueError("Negative epochs")
    vocabulary = ["cat", "kitten", "dog", "puppy", "car", "bus"]
    rng = random.Random(seed)
    targets = {word: [rng.uniform(-0.2, 0.2) for _ in range(3)] for word in vocabulary}
    contexts = {word: [rng.uniform(-0.2, 0.2) for _ in range(3)] for word in vocabulary}
    positives = [("cat", "kitten"), ("kitten", "cat"), ("dog", "puppy"), ("puppy", "dog"), ("car", "bus"), ("bus", "car")]
    examples = [(a, b, 1) for a, b in positives] + [(a, b, 0) for a, b in [("cat", "bus"), ("kitten", "car"), ("dog", "car"), ("puppy", "bus"), ("car", "cat"), ("bus", "dog")]]
    def objective():
        return sum(binary_logit_loss(dot(targets[a], contexts[b]), label) for a, b, label in examples) / len(examples)
    initial = objective()
    for _ in range(epochs):
        for a, b, label in examples:
            skipgram_step(targets[a], contexts[b], label)
    return {"initial_loss": initial, "final_loss": objective(), "target_vectors": targets, "context_vectors": contexts}


def contrastive_loss(scores, temperature=0.1):
    """One positive at index 0, all other logits negative. Stable InfoNCE."""
    scores = vector(scores)
    if len(scores) < 2 or not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("Positive temperature and at least one negative required")
    logits = [score / temperature for score in scores]
    maximum = max(logits)
    exponents = [math.exp(value - maximum) for value in logits]
    denominator = sum(exponents)
    probabilities = [value / denominator for value in exponents]
    loss = maximum + math.log(denominator) - logits[0]
    return loss, probabilities


def mean_pool(hidden, mask):
    if not hidden or len(hidden) != len(mask) or any(value not in (0, 1) for value in mask):
        raise ValueError("Matching token states and binary mask required")
    width = len(vector(hidden[0]))
    hidden = [vector(row, width) for row in hidden]
    denominator = sum(mask)
    if denominator == 0:
        raise ValueError("Cannot pool an entirely masked sequence")
    return [sum(row[j] * m for row, m in zip(hidden, mask)) / denominator for j in range(width)]


def centroids(vectors, labels):
    if len(vectors) != len(labels) or not vectors:
        raise ValueError("Labeled training vectors required")
    width = len(vector(vectors[0]))
    grouped = defaultdict(list)
    for values, label in zip(vectors, labels):
        grouped[label].append(unit(vector(values, width)))
    return {label: unit([sum(row[j] for row in rows) / len(rows) for j in range(width)]) for label, rows in grouped.items()}


def classify(values, prototypes):
    if not prototypes:
        raise ValueError("No class prototypes")
    return min(((label, cosine(values, prototype)) for label, prototype in prototypes.items()), key=lambda row: (-row[1], row[0]))


def kmeans(points, k, max_iterations=50):
    if not points or not isinstance(k, int) or not 1 <= k <= len(points) or max_iterations < 1:
        raise ValueError("Valid points, k, and iteration budget required")
    width = len(vector(points[0]))
    points = [vector(point, width) for point in points]
    if len({tuple(point) for point in points}) < k:
        raise ValueError("Need at least k distinct points")
    # Deterministic farthest-first initialization; not k-means++ sampling.
    centers = [points[0][:]]
    while len(centers) < k:
        centers.append(max(points, key=lambda point: min(euclidean(point, center) for center in centers))[:])
    for _ in range(max_iterations):
        labels = [min(range(k), key=lambda i: euclidean(point, centers[i])) for point in points]
        updated = []
        for index in range(k):
            members = [point for point, label in zip(points, labels) if label == index]
            if members:
                updated.append([sum(point[j] for point in members) / len(members) for j in range(width)])
            else:
                updated.append(max(points, key=lambda point: min(euclidean(point, center) for center in centers))[:])
        movement = max(euclidean(a, b) for a, b in zip(centers, updated))
        centers = updated
        if movement < 1e-10:
            break
    labels = [min(range(k), key=lambda i: euclidean(point, centers[i])) for point in points]
    inertia = sum(euclidean(point, centers[label]) ** 2 for point, label in zip(points, labels))
    return centers, labels, inertia


def silhouette(points, labels):
    if len(points) != len(labels) or not 1 < len(set(labels)) < len(points):
        raise ValueError("Require 2 through n-1 clusters")
    groups = {label: [i for i, group in enumerate(labels) if group == label] for label in set(labels)}
    values = []
    for index, point in enumerate(points):
        same = [i for i in groups[labels[index]] if i != index]
        if not same:
            values.append(0.0)
            continue
        a = sum(euclidean(point, points[i]) for i in same) / len(same)
        b = min(sum(euclidean(point, points[i]) for i in ids) / len(ids) for label, ids in groups.items() if label != labels[index])
        values.append((b - a) / max(a, b) if max(a, b) else 0.0)
    return sum(values) / len(values)


def binary_metrics(labels, scores, threshold):
    if len(labels) != len(scores) or any(label not in (0, 1) for label in labels) or not math.isfinite(threshold):
        raise ValueError("Matching binary labels and scores required")
    if any(not math.isfinite(score) for score in scores):
        raise ValueError("Finite scores required")
    predicted = [score >= threshold for score in scores]
    tp = sum(bool(label) and prediction for label, prediction in zip(labels, predicted))
    fp = sum(not label and prediction for label, prediction in zip(labels, predicted))
    fn = sum(label and not prediction for label, prediction in zip(labels, predicted))
    tn = len(labels) - tp - fp - fn
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": precision, "recall": recall,
            "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0}


def nearest_neighbor_outlier_scores(points):
    if len(points) < 2:
        raise ValueError("At least two points required")
    return [min(euclidean(point, other) for j, other in enumerate(points) if i != j) for i, point in enumerate(points)]


def retrieval_metrics(ranking, relevant, k=3):
    if k < 1:
        raise ValueError("Positive k required")
    seen, matches = set(), []
    for identity in ranking[:k]:
        matches.append(identity in relevant and identity not in seen)
        seen.add(identity)
    first = next((1 / i for i, hit in enumerate(matches, 1) if hit), 0.0)
    return {"precision": sum(matches) / k, "recall": sum(matches) / len(relevant) if relevant else 0.0, "mrr": first}


def pca_2d(points):
    """Actual 2D-to-1D PCA, population covariance; sign fixed for reproducibility."""
    if len(points) < 2:
        raise ValueError("At least two 2D points required")
    points = [vector(point, 2) for point in points]
    mean = [sum(point[j] for point in points) / len(points) for j in range(2)]
    centered = [[point[j] - mean[j] for j in range(2)] for point in points]
    a = sum(point[0] ** 2 for point in centered) / len(points)
    b = sum(point[0] * point[1] for point in centered) / len(points)
    c = sum(point[1] ** 2 for point in centered) / len(points)
    discriminant = math.hypot(a - c, 2 * b)
    eigenvalue = (a + c + discriminant) / 2
    if abs(b) > 1e-14:
        component = unit([b, eigenvalue - a])
    else:
        component = [1.0, 0.0] if a >= c else [0.0, 1.0]
    if next((x for x in component if abs(x) > 1e-14), 1) < 0:
        component = [-x for x in component]
    projected = [dot(point, component) for point in centered]
    return {"mean": mean, "component": component, "projected": projected,
            "explained_variance_ratio": eigenvalue / (a + c) if a + c else 0.0}


def quantize_int8(values):
    values = vector(values)
    maximum = max(abs(x) for x in values)
    scale = maximum / 127 if maximum else 1.0
    quantized = [max(-127, min(127, round(x / scale))) for x in values]
    return quantized, scale


def dequantize_int8(quantized, scale):
    if not math.isfinite(scale) or scale <= 0 or any(not isinstance(x, int) or not -127 <= x <= 127 for x in quantized):
        raise ValueError("Valid int8 codes and positive scale required")
    return [x * scale for x in quantized]


@dataclass(frozen=True)
class EmbeddingSpec:
    provider: str
    model: str
    revision: str
    dimensions: int
    query_recipe: str
    document_recipe: str
    normalization: str = "l2"
    preprocessing: str = "NFC-v1"

    def fingerprint(self):
        if not isinstance(self.dimensions, int) or self.dimensions < 1:
            raise ValueError("Positive dimensions required")
        payload = json.dumps(asdict(self), sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(payload.encode()).hexdigest()


def cache_key(text, spec, role):
    if role not in {"query", "document"}:
        raise ValueError("Unknown encoder role")
    # Must correspond to the encoder's actual preprocessing contract.
    normalized = unicodedata.normalize("NFC", text)
    return hashlib.sha256(json.dumps([normalized, spec.fingerprint(), role], ensure_ascii=False).encode()).hexdigest()


def save_vector(connection, identity, values, spec):
    values = vector(values, spec.dimensions)
    fingerprint = spec.fingerprint()
    connection.execute("CREATE TABLE IF NOT EXISTS embeddings (id TEXT, spec TEXT, payload TEXT, PRIMARY KEY(id,spec))")
    with connection:
        connection.execute("INSERT INTO embeddings VALUES(?,?,?) ON CONFLICT(id,spec) DO UPDATE SET payload=excluded.payload",
                           (identity, fingerprint, json.dumps(values)))


def read_vector(connection, identity, spec):
    connection.execute("CREATE TABLE IF NOT EXISTS embeddings (id TEXT, spec TEXT, payload TEXT, PRIMARY KEY(id,spec))")
    row = connection.execute("SELECT payload FROM embeddings WHERE id=? AND spec=?", (identity, spec.fingerprint())).fetchone()
    return vector(json.loads(row[0]), spec.dimensions) if row else None


def load_data():
    return json.loads((Path(__file__).parent / "data" / "courses.json").read_text(encoding="utf-8"))


def workbench(query, k=3):
    rows = load_data()
    encoder = Tfidf().fit([row["text"] for row in rows])
    values = [encoder.transform(row["text"]) for row in rows]
    query_vector = encoder.transform(query)
    hits = [(rows[index], score) for index, score in search(query_vector, values, k) if score > 0]
    return {"mode": "offline_lexical_tfidf", "dimensions": len(encoder.vocabulary),
            "query": query, "hits": [{"id": row["id"], "score": score, "text": row["text"]} for row, score in hits]}
