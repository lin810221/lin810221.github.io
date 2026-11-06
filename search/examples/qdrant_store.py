"""Real Qdrant Local API. Local mode does NOT benchmark server-side HNSW."""
from collections import Counter
from qdrant_client import QdrantClient, models
from search_core import DIMENSION, RECIPE, Document, fixture_vector, fixtures, tokenize

COLLECTION = "learningnote_fixture8_v1"
VOCABULARY = {term: index for index, term in enumerate(sorted({term for doc in fixtures() for term in tokenize(doc.title+" "+doc.body)}))}


def sparse(text):
    counts = Counter(tokenize(text))
    pairs = sorted((VOCABULARY[term], float(count)) for term,count in counts.items() if term in VOCABULARY)
    return models.SparseVector(indices=[key for key,value in pairs], values=[value for key,value in pairs])


def tenant_filter(tenant, recipe=RECIPE):
    if not isinstance(tenant,str) or not tenant: raise ValueError("Trusted tenant required")
    return models.Filter(must=[models.FieldCondition(key="tenant",match=models.MatchValue(value=tenant)),
        models.FieldCondition(key="active",match=models.MatchValue(value=True)),
        models.FieldCondition(key="recipe",match=models.MatchValue(value=recipe))])


class VectorStore:
    def __init__(self, path=None, collection=COLLECTION):
        self.collection = collection
        self.client = QdrantClient(path=str(path)) if path else QdrantClient(location=":memory:")
        if not self.client.collection_exists(collection):
            self.client.create_collection(collection,
                vectors_config={"dense":models.VectorParams(size=DIMENSION,distance=models.Distance.COSINE)},
                sparse_vectors_config={"lexical":models.SparseVectorParams()})
        params = self.client.get_collection(collection).config.params.vectors
        if params["dense"].size != DIMENSION or params["dense"].distance != models.Distance.COSINE:
            self.close(); raise ValueError("Collection vector contract mismatch")

    def __enter__(self): return self
    def __exit__(self,*args): self.close()
    def close(self): self.client.close()

    def upsert(self, doc: Document, recipe=RECIPE):
        if recipe != RECIPE: raise ValueError("Different embedding recipe requires another generation")
        point = models.PointStruct(id=doc.point_id,
            vector={"dense":fixture_vector(doc.title+" "+doc.body),"lexical":sparse(doc.title+" "+doc.body)},
            payload={"tenant":doc.tenant,"doc_id":doc.doc_id,"revision":doc.revision,"active":doc.active,"recipe":recipe})
        self.client.upsert(self.collection, points=[point], wait=True)

    def delete(self, point_id):
        self.client.delete(self.collection,points_selector=models.PointIdsList(points=[point_id]),wait=True)

    def query(self, tenant, text, k=5, hybrid=False):
        if type(k) is not int or not 1 <= k <= 100: raise ValueError("Bounded integer k required")
        boundary = tenant_filter(tenant)
        dense = fixture_vector(text)
        kwargs = dict(collection_name=self.collection,query_filter=boundary,limit=k,
                      with_payload=["tenant","doc_id","revision","active","recipe"],with_vectors=False)
        lexical = sparse(text)
        if hybrid and lexical.indices:
            candidates = min(100, max(10,k*3))
            return self.client.query_points(**kwargs,
                prefetch=[models.Prefetch(query=dense,using="dense",filter=boundary,limit=candidates),
                          models.Prefetch(query=lexical,using="lexical",filter=boundary,limit=candidates)],
                query=models.FusionQuery(fusion=models.Fusion.RRF)).points
        return self.client.query_points(**kwargs,query=dense,using="dense").points


def replay(source, vectors: VectorStore, fail_after_write=False):
    """Single ordered worker, at-least-once replay. Not a distributed CAS engine."""
    applied = 0
    for seq, event in source.events(source.checkpoint()):
        current = source.get(event.tenant,event.doc_id)
        # The authoritative source/tombstone defeats old upserts and replays.
        if current and current.revision == event.revision:
            if current.active: vectors.upsert(current)
            else: vectors.delete(current.point_id)
            applied += 1
            if fail_after_write: raise RuntimeError("Injected worker crash before checkpoint")
        source.acknowledge(seq)
    return applied


def rebuild_from_source(source, vectors: VectorStore):
    """Restore a NEW empty index from a stable offline source snapshot.

    An existing source checkpoint cannot prove a newly restored index is caught
    up. Concurrent producers require a snapshot/watermark protocol instead.
    """
    docs = source.documents()
    for doc in docs:
        if doc.active: vectors.upsert(doc)
    events = source.events()
    if events: source.acknowledge(events[-1][0])
    return sum(doc.active for doc in docs)
