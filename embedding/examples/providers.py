"""Optional HTTP encoders. Only explicitly selected live entrypoints call these."""
import json
import math
import os
import re
import urllib.error
import urllib.request


def post(url, payload, key_name, header_name):
    key = os.environ.get(key_name)
    if not key:
        raise ValueError(f"Set {key_name} in your terminal environment")
    header = "Bearer " + key if header_name == "Authorization" else key
    request = urllib.request.Request(url, data=json.dumps(payload).encode(),
        headers={header_name: header, "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"Embedding service returned HTTP {error.code}; no automatic retry") from None


def validate_batch(vectors, count, dimensions=None):
    if len(vectors) != count or not vectors or not vectors[0]:
        raise ValueError("Embedding count/shape mismatch")
    width = dimensions if dimensions is not None else len(vectors[0])
    if any(len(row) != width or any(not math.isfinite(value) for value in row) for row in vectors):
        raise ValueError("Embedding dimensions or values invalid")
    return vectors


def validate_inputs(texts, dimensions):
    if not texts or any(not isinstance(text, str) or not text.strip() for text in texts):
        raise ValueError("Nonempty text inputs required")
    if dimensions is not None and (not isinstance(dimensions, int) or dimensions < 1):
        raise ValueError("Positive dimensions required")


def openai_payload(texts, model="text-embedding-3-small", dimensions=None):
    validate_inputs(texts, dimensions)
    payload = {"model": model, "input": texts, "encoding_format": "float"}
    if dimensions is not None:
        payload["dimensions"] = dimensions
    return payload


def openai_embeddings(texts, model="text-embedding-3-small", dimensions=None):
    result = post("https://api.openai.com/v1/embeddings", openai_payload(texts, model, dimensions),
                  "OPENAI_API_KEY", "Authorization")
    rows = sorted(result.get("data", []), key=lambda row: row["index"])
    if [row["index"] for row in rows] != list(range(len(texts))):
        raise ValueError("Embedding response indices mismatch")
    return validate_batch([row["embedding"] for row in rows], len(texts), dimensions)


def gemini_payload(texts, model="gemini-embedding-001", task="RETRIEVAL_DOCUMENT", dimensions=None):
    validate_inputs(texts, dimensions)
    if not re.fullmatch(r"[a-zA-Z0-9_.-]+", model):
        raise ValueError("Model must be a resource basename")
    if task not in {"RETRIEVAL_QUERY", "RETRIEVAL_DOCUMENT", "SEMANTIC_SIMILARITY", "CLASSIFICATION", "CLUSTERING"}:
        raise ValueError("Unsupported teaching task")
    config = {"taskType": task}
    if dimensions is not None:
        config["outputDimensionality"] = dimensions
    # Current REST schema: nested config, rather than deprecated request fields.
    return {"requests": [{"model": "models/" + model, "content": {"parts": [{"text": text}]},
                           "embedContentConfig": dict(config)} for text in texts]}


def gemini_embeddings(texts, model="gemini-embedding-001", task="RETRIEVAL_DOCUMENT", dimensions=None):
    payload = gemini_payload(texts, model, task, dimensions)
    result = post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:batchEmbedContents",
                  payload, "GEMINI_API_KEY", "x-goog-api-key")
    # Gemini documents the same order as the input requests (no per-row index).
    return validate_batch([row["values"] for row in result.get("embeddings", [])], len(texts), dimensions)
