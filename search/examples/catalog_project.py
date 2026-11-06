"""Search engineering project: FTS5 + Qdrant + source revalidation + RRF."""
from dataclasses import dataclass
from search_core import RECIPE, fixtures, rrf
from source_store import SourceStore
from qdrant_store import VectorStore, replay


@dataclass(frozen=True)
class Principal:
    tenant: str
    scopes: frozenset[str]


ALPHA = Principal("alpha",frozenset({"catalog:read"}))
BETA = Principal("beta",frozenset({"catalog:read"}))


class CatalogSearch:
    def __init__(self, source, vectors, principal):
        self.source,self.vectors,self.principal = source,vectors,principal

    def search(self, text, k=5):
        principal = self.principal
        if not principal.tenant or "catalog:read" not in principal.scopes:
            raise PermissionError("Verified tenant and catalog:read are required")
        if not isinstance(text,str) or not text.strip() or len(text)>200 or type(k) is not int or not 1<=k<=20:
            raise ValueError("Nonblank query <=200 characters and k within 1..20 required")
        budget = min(100,max(10,k*3))
        lexical = self.source.search(principal.tenant,text,budget)
        hydrated = {doc.point_id:doc for doc,score in lexical}
        accepted,discarded = [],0
        for point in self.vectors.query(principal.tenant,text,budget):
            payload = point.payload or {}
            current = self.source.by_point(principal.tenant,point.id) if type(point.id) is int else None
            if (not current or not current.active or payload.get("tenant")!=principal.tenant
                or payload.get("doc_id")!=current.doc_id or payload.get("recipe")!=RECIPE
                or type(payload.get("revision")) is not int or payload["revision"]!=current.revision):
                discarded += 1
                continue
            hydrated[point.id] = current
            accepted.append((point.id,float(point.score)))
        fused = rrf([[(d.point_id,score) for d,score in lexical],accepted])[:k]
        return {"hits":[{"point_id":point_id,"doc_id":hydrated[point_id].doc_id,
                         "title":hydrated[point_id].title,"revision":hydrated[point_id].revision,
                         "fusion_score":score} for point_id,score in fused],
                "discarded_stale_or_ineligible":discarded,"recipe":RECIPE,
                "mode":"SQLite FTS5 + Qdrant Local exact dense candidates + application RRF"}


def seed(source):
    for doc in fixtures(): source.upsert(doc)


def build_demo(source_path=":memory:",vector_path=None):
    source = SourceStore(source_path)
    try:
        seed(source)
        vectors = VectorStore(vector_path)
        try:
            replay(source,vectors)
        except BaseException:
            vectors.close(); raise
        return source,vectors
    except BaseException:
        source.close(); raise
