"""Elasticsearch request construction and psycopg plans. Default is offline."""
import json
from typing import NamedTuple
from elasticsearch import Elasticsearch
from elastic_transport import BaseNode, ApiResponseMeta, HttpHeaders
from search_core import DIMENSION, RECIPE, fixture_vector


def elastic_mapping():
    return {"dynamic":"strict","properties":{
        "tenant":{"type":"keyword"},"doc_id":{"type":"keyword"},"point_id":{"type":"long"},
        "title":{"type":"text","fields":{"raw":{"type":"keyword"}}},"body":{"type":"text"},
        "category":{"type":"keyword"},"active":{"type":"boolean"},"revision":{"type":"long"},
        "recipe":{"type":"keyword"},"embedding":{"type":"dense_vector","dims":DIMENSION,"similarity":"cosine"}}}


def elastic_query(tenant, text, k=5):
    if not tenant or type(k) is not int or not 1 <= k <= 100: raise ValueError("Trusted tenant and bounded size required")
    return {"size":k,"query":{"bool":{"must":[{"multi_match":{"query":text,"fields":["title^2","body"]}}],
        "filter":[{"term":{"tenant":tenant}},{"term":{"active":True}},{"term":{"recipe":RECIPE}}]}},
        "_source":["doc_id","title","revision"],"sort":[{"_score":"desc"},{"point_id":"asc"}]}


def elastic_knn(tenant, text, k=5, candidates=30):
    if type(k) is not int or type(candidates) is not int or not 1 <= k <= candidates <= 1000:
        raise ValueError("Require 1 <= k <= num_candidates <= 1000")
    return {"knn":{"field":"embedding","query_vector":fixture_vector(text),"k":k,"num_candidates":candidates,
        "filter":{"bool":{"filter":[{"term":{"tenant":tenant}},{"term":{"active":True}},{"term":{"recipe":RECIPE}}]}}},"size":k}


class RecordedResponse(NamedTuple):
    meta: ApiResponseMeta
    body: bytes


class RecordingNode(BaseNode):
    """Tests the real SDK serializer without a socket or an Elasticsearch server."""
    calls = []

    def perform_request(self,method,target,body=None,headers=None,request_timeout=None):
        type(self).calls.append({"method":method,"target":target,"body":body})
        response = {"acknowledged":True,"errors":False,"items":[],"id":"mock-pit-id",
                    "hits":{"hits":[],"total":{"value":0,"relation":"eq"}}}
        meta = ApiResponseMeta(status=200,http_version="1.1",
            headers=HttpHeaders({"content-type":"application/json","x-elastic-product":"Elasticsearch"}),
            duration=0.001,node=self.config)
        return RecordedResponse(meta,json.dumps(response).encode())

    def close(self): pass


def recording_client():
    RecordingNode.calls = []
    return Elasticsearch("http://127.0.0.1:9200",node_class=RecordingNode)


PG_QUERY = """SELECT point_id,doc_id,title,embedding <=> %s::vector AS distance
FROM search_documents
WHERE tenant=%s AND active
ORDER BY embedding <=> %s::vector
LIMIT %s"""


def pg_parameters(tenant, text, k=5):
    if not tenant or type(k) is not int or not 1 <= k <= 100: raise ValueError("Trusted tenant and bounded limit required")
    vector = fixture_vector(text)
    return (vector,tenant,vector,k)
