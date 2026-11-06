"""Actual Faiss CPU indexes. Tiny seeded experiments, not product benchmarks."""
from hashlib import sha256
from pathlib import Path
from time import perf_counter
import json
import faiss
import numpy as np
from search_core import ann_recall, matrix, normalize

# Deterministic teaching runs; production thread counts must be measured.
faiss.omp_set_num_threads(1)


def sample(n=2048, dimension=32, queries=12):
    rng = np.random.default_rng(41)
    return normalize(rng.normal(size=(n,dimension))), normalize(rng.normal(size=(queries,dimension)))


def flat(vectors):
    values = matrix(vectors)
    index = faiss.IndexFlatIP(values.shape[1])
    index.add(values)
    return index


def hnsw(vectors, neighbors=16, construction=64, ef_search=32):
    values = matrix(vectors)
    if min(neighbors,construction,ef_search) < 1: raise ValueError("Positive HNSW parameters required")
    index = faiss.IndexHNSWFlat(values.shape[1],neighbors,faiss.METRIC_INNER_PRODUCT)
    index.hnsw.efConstruction = construction
    index.hnsw.efSearch = ef_search
    index.add(values)
    return index


def ivfpq(vectors, nlist=16, subquantizers=4, bits=4, nprobe=4):
    values = matrix(vectors)
    if values.shape[1] % subquantizers or not 1 <= nprobe <= nlist:
        raise ValueError("Dimension must divide into subquantizers; nprobe must fit nlist")
    if len(values) < 40 * max(nlist,2**bits):
        raise ValueError("This teaching configuration needs enough training vectors")
    index = faiss.IndexIVFPQ(faiss.IndexFlatIP(values.shape[1]), values.shape[1],
                            nlist,subquantizers,bits,faiss.METRIC_INNER_PRODUCT)
    index.train(values)
    index.add(values)
    index.nprobe = nprobe
    return index


def evaluate(index, exact, queries, k=5):
    queries = matrix(queries,index.d)
    _, reference = exact.search(queries,min(k,exact.ntotal))
    index.search(queries[:1],k)  # Warm-up is excluded from latency samples.
    latencies, recalls = [], []
    for query, truth in zip(queries,reference):
        start = perf_counter()
        _, result = index.search(query.reshape(1,-1),k)
        latencies.append((perf_counter()-start)*1000)
        recalls.append(ann_recall([int(i) for i in truth if i >= 0], [int(i) for i in result[0] if i >= 0],k))
    return {"queries":len(queries),"recall_mean":float(np.mean([r for r in recalls if r is not None])),
            "p50_ms":float(np.percentile(latencies,50)),"p95_ms":float(np.percentile(latencies,95)),
            "timing_scope":"local CPU index.search only; no network, model or production claim"}


def save_trusted(index, folder: Path):
    folder.mkdir(parents=True,exist_ok=False)
    raw = faiss.serialize_index(index).tobytes()
    (folder/"index.bin").write_bytes(raw)
    manifest = {"sha256":sha256(raw).hexdigest(),"dimension":index.d,"count":index.ntotal,"metric":"inner_product"}
    (folder/"manifest.json").write_text(json.dumps(manifest),encoding="utf-8")
    return manifest


def load_trusted(folder: Path, expected_dimension):
    # Both files must come from a trusted location. A hash is not a signature.
    manifest = json.loads((folder/"manifest.json").read_text(encoding="utf-8"))
    raw = (folder/"index.bin").read_bytes()
    if len(raw) > 32*1024*1024 or sha256(raw).hexdigest() != manifest["sha256"] or manifest["dimension"] != expected_dimension:
        raise ValueError("Artifact checksum, dimension or size contract failed")
    index = faiss.deserialize_index(np.frombuffer(raw,dtype="uint8").copy())
    if index.d != expected_dimension or index.ntotal != manifest["count"]:
        raise ValueError("Index metadata mismatch")
    return index
