"""Real FTS5/Faiss/Qdrant Local acceptance; ES serialization; PG SQL inspection.

No model calls, network services or automatic Docker downloads.
"""
from dataclasses import replace
from importlib import import_module
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import json
import apsw
import unittest
import numpy as np
from search_core import (Document,fixtures,tokenize,han_bigrams,postings,bm25,normalize,exact_topk,
                         rrf,linear_fusion,ann_recall,ndcg,capacity,fixture_vector,RECIPE)
from source_store import SourceStore
from qdrant_store import VectorStore,replay,rebuild_from_source
from vector_indexes import sample,flat,hnsw,ivfpq,evaluate,save_trusted,load_trusted
from engine_clients import elastic_mapping,elastic_query,elastic_knn,recording_client,RecordingNode,PG_QUERY,pg_parameters
from catalog_project import ALPHA,BETA,Principal,CatalogSearch,build_demo
from generations import IndexRegistry


class TextTests(unittest.TestCase):
    def test_unicode_normalization_and_case(self):
        self.assertEqual(tokenize("ＵＳＢ-C"),["usb","c"])

    def test_han_bigrams_are_explicitly_different(self):
        self.assertEqual(tokenize("向量資料"),["向量資料"])
        self.assertEqual(han_bigrams("向量資料"),["向量","量資","資料"])

    def test_postings_keep_positions(self):
        self.assertEqual(postings({"a":"usb hub usb"})["usb"]["a"],[0,2])

    def test_bm25_no_query_match(self):
        self.assertTrue(all(value==0 for _,value in bm25({"a":"usb","b":"hub"},"missing")))

    def test_bm25_tf_saturates(self):
        scores=dict(bm25({"one":"hub","many":"hub "*10},"hub",b=0))
        self.assertGreater(scores["many"],scores["one"])
        self.assertLess(scores["many"],10*scores["one"])

    def test_bm25_length_normalization(self):
        rows=bm25({"short":"hub","long":"hub "+"manual "*50},"hub",b=1)
        self.assertEqual(rows[0][0],"short")

    def test_bm25_bad_parameters(self):
        for args in ({"k1":0},{"b":2},{"b":float("nan")}):
            with self.subTest(args=args),self.assertRaises(ValueError): bm25({"a":"hub"},"hub",**args)


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.store=SourceStore(); self.addCleanup(self.store.close)
        for doc in fixtures(): self.store.upsert(doc)

    def test_fts_returns_eligible_documents(self):
        rows=self.store.search("alpha","usb hub")
        self.assertEqual([doc.doc_id for doc,score in rows],["AX-100"])

    def test_same_logical_id_is_tenant_scoped(self):
        self.assertEqual(self.store.get("alpha","AX-100").point_id,1001)
        self.assertEqual(self.store.get("beta","AX-100").point_id,2001)

    def test_fts_operator_text_does_not_escape_scope(self):
        for query in ('usb OR confidential','" OR 1=1 --',"usb NEAR beta"):
            rows=self.store.search("alpha",query)
            self.assertTrue(all(doc.tenant=="alpha" and doc.active for doc,score in rows))

    def test_fts_update_removes_old_terms(self):
        doc=self.store.get("alpha","AX-100")
        self.store.upsert(replace(doc,title="Unique revision",body="brandnewtoken",revision=2))
        self.assertNotIn(1001,[d.point_id for d,s in self.store.search("alpha","usb")])
        self.assertEqual(self.store.search("alpha","brandnewtoken")[0][0].revision,2)

    def test_tombstone_filters_lexical_results(self):
        self.store.tombstone("alpha","AX-100",2)
        self.assertEqual(self.store.search("alpha","usb hub"),[])
        self.assertFalse(self.store.get("alpha","AX-100").active)

    def test_same_revision_same_content_is_idempotent(self):
        before=len(self.store.events())
        self.assertFalse(self.store.upsert(fixtures()[0]))
        self.assertEqual(len(self.store.events()),before)

    def test_same_revision_different_content_conflicts(self):
        with self.assertRaises(ValueError): self.store.upsert(replace(fixtures()[0],title="changed"))

    def test_stale_revision_cannot_resurrect_delete(self):
        self.store.tombstone("alpha","AX-100",2)
        with self.assertRaises(ValueError): self.store.upsert(fixtures()[0])

    def test_stable_point_id_cannot_change(self):
        with self.assertRaises(ValueError): self.store.upsert(replace(fixtures()[0],point_id=9999,revision=2))

    def test_source_and_outbox_rollback_together(self):
        with SourceStore() as source:
            source.conn.execute("CREATE TRIGGER stop_event BEFORE INSERT ON outbox BEGIN SELECT RAISE(ABORT,'injected failure'); END;")
            with self.assertRaises(apsw.ConstraintError): source.upsert(fixtures()[0])
            self.assertEqual(source.documents(),[]); self.assertEqual(source.events(),[])
            self.assertEqual(source.search("alpha","usb"),[])

    def test_backup_preserves_fts_and_revisions(self):
        with TemporaryDirectory() as folder:
            path=Path(folder)/"backup.sqlite"
            self.store.backup(path)
            with SourceStore(path) as restored:
                self.assertEqual(restored.search("alpha","usb hub")[0][0].point_id,1001)
                self.assertEqual(len(restored.events()),10)

    def test_bounded_limit_rejects_bool_and_zero(self):
        for k in (0,True,101):
            with self.subTest(k=k),self.assertRaises(ValueError): self.store.search("alpha","usb",k)


class VectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vectors,cls.queries=sample()
        cls.exact=flat(cls.vectors)

    def test_zero_and_nonfinite_vectors_rejected(self):
        for values in ([[0,0]],[[float("nan"),1]],[[float("inf"),1]]):
            with self.subTest(values=values),self.assertRaises(ValueError): normalize(values)

    def test_exact_metric_orientation(self):
        values=[[1,0],[0,1],[-1,0]]
        self.assertEqual(exact_topk(values,[1,0],3,metric="dot")[0][0],0)
        self.assertEqual(exact_topk(values,[1,0],3,metric="l2")[0][0],0)
        self.assertEqual(exact_topk(values,[1,0],3,metric="cosine")[0][0],0)

    def test_exact_filter_precedes_topk(self):
        self.assertEqual(exact_topk([[1,0],[0.9,0.1],[0,1]],[1,0],2,eligible=[2]),[(2,0.0)])

    def test_dimension_mismatch_rejected(self):
        with self.assertRaises(ValueError): exact_topk([[1,0]],[1,0,0])

    def test_flat_matches_numpy(self):
        _,ids=self.exact.search(self.queries[:1],5)
        wanted=[i for i,s in exact_topk(self.vectors,self.queries[0],5,metric="dot")]
        self.assertEqual(ids[0].tolist(),wanted)

    def test_real_hnsw_recall_against_exact(self):
        report=evaluate(hnsw(self.vectors,ef_search=128),self.exact,self.queries)
        self.assertGreaterEqual(report["recall_mean"],0.75)
        self.assertLessEqual(report["recall_mean"],1)
        self.assertGreaterEqual(report["p95_ms"],0)

    def test_real_ivfpq_trains_and_searches(self):
        index=ivfpq(self.vectors)
        self.assertTrue(index.is_trained); self.assertEqual(index.ntotal,len(self.vectors))
        self.assertTrue(0<=evaluate(index,self.exact,self.queries)["recall_mean"]<=1)

    def test_ivfpq_rejects_invalid_training_contract(self):
        with self.assertRaises(ValueError): ivfpq(self.vectors,subquantizers=3)
        with self.assertRaises(ValueError): ivfpq(self.vectors[:100])

    def test_trusted_index_roundtrip(self):
        with TemporaryDirectory() as folder:
            path=Path(folder)/"index"; save_trusted(self.exact,path)
            restored=load_trusted(path,32)
            self.assertEqual(restored.ntotal,self.exact.ntotal)
            self.assertEqual(restored.search(self.queries[:1],3)[1].tolist(),self.exact.search(self.queries[:1],3)[1].tolist())

    def test_corrupt_artifact_rejected_before_deserialize(self):
        with TemporaryDirectory() as folder:
            path=Path(folder)/"index"; save_trusted(self.exact,path)
            (path/"index.bin").write_bytes(b"corrupt")
            with self.assertRaises(ValueError): load_trusted(path,32)


class FusionTests(unittest.TestCase):
    def test_rrf_uses_rank_not_score_magnitude(self):
        first=rrf([[(1,100),(2,1)],[(2,.9),(1,.8)]])
        second=rrf([[(1,1e9),(2,0)],[(2,9),(1,-3)]])
        self.assertEqual(first,second)

    def test_zero_weight_disables_branch(self):
        self.assertEqual([key for key,s in rrf([[(1,2)],[(2,.9)]],weights=[1,0])],[1])

    def test_duplicates_cannot_gain_extra_rrf_score(self):
        with self.assertRaises(ValueError): rrf([[(1,2),(1,1)]])

    def test_linear_fusion_normalizes_each_branch(self):
        result=linear_fusion([[(1,100),(2,0)],[(2,.9),(1,.8)]],[.8,.2])
        self.assertEqual(result[0][0],1)

    def test_invalid_weights_rejected(self):
        with self.assertRaises(ValueError): rrf([[(1,1)]],weights=[-1])
        with self.assertRaises(ValueError): linear_fusion([[(1,1)]],[0])

    def test_ann_recall_eligible_denominator(self):
        self.assertEqual(ann_recall([1,2],[1],10),.5)
        self.assertIsNone(ann_recall([],[],5))

    def test_ndcg_perfect_and_incomplete(self):
        qrels={1:3,2:1,3:0}
        self.assertEqual(ndcg([1,2,3],qrels,3),1)
        self.assertLess(ndcg([3,2,1],qrels,3),1)
        self.assertIsNone(ndcg([1],{},3))

    def test_capacity_counts_retained_originals(self):
        raw=capacity(1000000,1536,bits=32)
        compressed=capacity(1000000,1536,bits=8,keep_original=True)
        self.assertEqual(raw["vectors"],6144000000)
        self.assertGreater(compressed["estimated_bytes"],raw["estimated_bytes"])


class QdrantTests(unittest.TestCase):
    def setUp(self):
        self.vectors=VectorStore(); self.addCleanup(self.vectors.close)
        for doc in fixtures(): self.vectors.upsert(doc)

    def test_dense_query_filters_tenant_and_active(self):
        hits=self.vectors.query("alpha","usb hub",10)
        self.assertTrue(hits)
        self.assertTrue(all(p.payload["tenant"]=="alpha" and p.payload["active"] for p in hits))

    def test_actual_named_sparse_dense_fusion(self):
        hits=self.vectors.query("alpha","usb hub",3,True)
        self.assertEqual(hits[0].id,1001)
        self.assertTrue(all(p.payload["tenant"]=="alpha" for p in hits))

    def test_wrong_recipe_upsert_rejected(self):
        with self.assertRaises(ValueError): self.vectors.upsert(fixtures()[0],recipe="other")

    def test_query_is_bounded(self):
        with self.assertRaises(ValueError): self.vectors.query("alpha","usb",101)

    def test_delete_removes_point(self):
        self.vectors.delete(1001)
        self.assertNotIn(1001,[p.id for p in self.vectors.query("alpha","usb hub",10)])

    def test_persistent_local_reopen(self):
        with TemporaryDirectory() as folder:
            path=Path(folder)/"vectors"
            with VectorStore(path) as store: store.upsert(fixtures()[0])
            with VectorStore(path) as restored: self.assertEqual(restored.query("alpha","usb hub",1)[0].id,1001)


class ReplayProjectTests(unittest.TestCase):
    def setUp(self):
        self.source,self.vectors=build_demo()
        self.addCleanup(self.source.close); self.addCleanup(self.vectors.close)

    def test_project_result_hydrates_current_source(self):
        hits=CatalogSearch(self.source,self.vectors,ALPHA).search("usb hub",3)["hits"]
        self.assertEqual(hits[0]["point_id"],1001)
        self.assertNotIn(2001,[h["point_id"] for h in hits])

    def test_beta_can_read_own_same_logical_identifier(self):
        hits=CatalogSearch(self.source,self.vectors,BETA).search("usb hub",3)["hits"]
        self.assertIn(2001,[h["point_id"] for h in hits])

    def test_missing_scope_rejected(self):
        with self.assertRaises(PermissionError): CatalogSearch(self.source,self.vectors,Principal("alpha",frozenset())).search("usb")

    def test_deleted_source_hidden_before_index_catches_up(self):
        self.source.tombstone("alpha","AX-100",2)
        report=CatalogSearch(self.source,self.vectors,ALPHA).search("usb hub",3)
        self.assertNotIn(1001,[h["point_id"] for h in report["hits"]])
        self.assertGreater(report["discarded_stale_or_ineligible"],0)

    def test_stale_vectors_do_not_replace_new_source_revision(self):
        self.source.upsert(replace(fixtures()[0],revision=2,title="Updated USB hub"))
        hits=CatalogSearch(self.source,self.vectors,ALPHA).search("usb hub",3)["hits"]
        self.assertTrue(all(h["revision"]==2 for h in hits if h["point_id"]==1001))

    def test_forged_cross_tenant_point_is_rejected_at_hydration(self):
        fake=SimpleNamespace(query=lambda *args:[SimpleNamespace(id=2001,score=1,payload={"tenant":"alpha","doc_id":"AX-100","revision":1,"recipe":RECIPE})])
        hits=CatalogSearch(self.source,fake,ALPHA).search("usb hub",3)["hits"]
        self.assertNotIn(2001,[h["point_id"] for h in hits])

    def test_crash_after_index_write_can_replay(self):
        self.source.upsert(replace(fixtures()[0],revision=2,title="Updated USB hub"))
        previous=self.source.checkpoint()
        with self.assertRaises(RuntimeError): replay(self.source,self.vectors,fail_after_write=True)
        self.assertEqual(self.source.checkpoint(),previous)
        replay(self.source,self.vectors)
        self.assertEqual(self.vectors.client.retrieve(self.vectors.collection,[1001])[0].payload["revision"],2)

    def test_replay_tombstone_does_not_resurrect_old_upsert(self):
        self.source.tombstone("alpha","AX-100",2)
        self.source.conn.execute("DELETE FROM checkpoints")
        replay(self.source,self.vectors)
        self.assertEqual(self.vectors.client.retrieve(self.vectors.collection,[1001]),[])

    def test_restore_new_index_requires_rebuild_not_old_checkpoint(self):
        with VectorStore(collection="fresh_generation") as fresh:
            self.assertEqual(replay(self.source,fresh),0)
            self.assertEqual(fresh.client.count(fresh.collection,exact=True).count,0)
            self.assertEqual(rebuild_from_source(self.source,fresh),9)
            self.assertEqual(fresh.client.count(fresh.collection,exact=True).count,9)

    def test_end_to_end_restore_report(self):
        with TemporaryDirectory() as folder:
            report=import_module("32_delivery_report").deliver(Path(folder)/"run")
            self.assertTrue(report["restore_matches"])
            self.assertNotIn(2001,report["alpha_ids"])


class EngineAndReleaseTests(unittest.TestCase):
    def test_es_mapping_has_exact_filter_fields(self):
        mapping=elastic_mapping()
        self.assertEqual(mapping["properties"]["tenant"]["type"],"keyword")
        self.assertEqual(mapping["properties"]["embedding"]["dims"],8)

    def test_real_es_sdk_serializes_scoped_query(self):
        with recording_client() as client: client.search(index="learningnote-catalog-v1",body=elastic_query("alpha","usb hub"))
        body=json.loads(RecordingNode.calls[-1]["body"])
        self.assertIn({"term":{"tenant":"alpha"}},body["query"]["bool"]["filter"])
        self.assertIn({"term":{"active":True}},body["query"]["bool"]["filter"])

    def test_knn_candidate_budget_checked(self):
        with self.assertRaises(ValueError): elastic_knn("alpha","usb",10,5)

    def test_pg_parameters_separate_sql_from_data(self):
        params=pg_parameters("alpha' OR 1=1 --","usb",3)
        self.assertEqual(params[1],"alpha' OR 1=1 --")
        self.assertNotIn(params[1],PG_QUERY)

    def test_pg_lab_schema_documents_rls_boundary(self):
        text=(Path(__file__).with_name("data")/"pg_schema.sql").read_text(encoding="utf-8")
        self.assertIn("vector_cosine_ops",text); self.assertIn("FORCE ROW LEVEL SECURITY",text)
        self.assertIn("non-BYPASSRLS",text)

    def test_unverified_generation_cannot_activate(self):
        with IndexRegistry() as registry:
            registry.register("v1","r1")
            with self.assertRaises(ValueError): registry.activate("v1",None,"r1")

    def test_generation_and_query_recipe_move_together(self):
        with IndexRegistry() as registry:
            registry.register("v1","r1")
            registry.verify("v1",dict(contract=True,scope=True,quality=True,checkpoint=True))
            with self.assertRaises(ValueError): registry.activate("v1",None,"wrong")
            self.assertEqual(registry.activate("v1",None,"r1"),{"generation":"v1","query_recipe":"r1"})
            with self.assertRaises(ValueError): registry.activate("v1",None,"r1")


if __name__ == "__main__": unittest.main(verbosity=2)

