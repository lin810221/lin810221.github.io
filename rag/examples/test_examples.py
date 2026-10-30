"""Behavioral tests for boundaries, security scope, metrics and API parsing.

All API responses are fixtures; no real API requests or model downloads.
"""
from dataclasses import replace
import importlib.util
import io
import json
import math
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import provider_http
from rag_core import (BM25, Document, all_chunks, ask, cache_key, chunk_document, cosine,
                      extractive_answer, load_documents, normalize, pack_context, read_store,
                      retrieval_metrics, retrieve, rrf, tokenize, upsert_document, validate_citations, visible)

HERE = Path(__file__).parent


class RAGTests(unittest.TestCase):
    def setUp(self):
        self.documents = load_documents()
        self.chunks = all_chunks()

    def test_normalize_unicode_and_newlines(self):
        self.assertEqual(normalize("  e\u0301\r\n申請\r完成  "), "é\n申請\n完成")

    def test_chunks_cover_source_and_have_correct_offsets(self):
        doc = Document("x", "範例", "一二三四五六七八九十甲乙丙丁")
        chunks = chunk_document(doc, 6, 2)
        covered = set()
        for chunk in chunks:
            self.assertEqual(chunk.text, doc.text[chunk.start:chunk.end])
            covered.update(range(chunk.start, chunk.end))
        self.assertEqual(covered, set(range(len(doc.text))))
        self.assertEqual(chunks[-1].end, len(doc.text))

    def test_chunk_boundary_exact_multiple_has_no_redundant_tail(self):
        self.assertEqual(len(chunk_document(Document("x", "x", "abcdefgh"), 4, 0)), 2)

    def test_invalid_chunk_parameters(self):
        for size, overlap in [(0, 0), (3, 3), (3, -1), (3.5, 0)]:
            with self.assertRaises(ValueError):
                chunk_document(self.documents[0], size, overlap)

    def test_empty_document(self):
        self.assertEqual(chunk_document(Document("x", "x", "  ")), [])

    def test_identity_is_stable_but_scoped_to_version_and_tenant(self):
        doc = self.documents[0]
        first = chunk_document(doc)[0].id
        self.assertEqual(first, chunk_document(doc)[0].id)
        self.assertNotEqual(first, chunk_document(replace(doc, tenant="other"))[0].id)
        self.assertNotEqual(first, chunk_document(replace(doc, version="new"))[0].id)

    def test_tokenizer_preserves_error_codes_and_chinese_bigrams(self):
        terms = tokenize("VPN-403 特休申請")
        self.assertIn("vpn-403", terms)
        self.assertIn("特休", terms)
        self.assertIn("申請", terms)

    def test_bm25_known_target(self):
        self.assertEqual(retrieve(self.chunks, "VPN-403")[0][0].doc_id, "it")

    def test_bm25_no_match_empty_and_k_zero(self):
        model = BM25(self.chunks)
        self.assertEqual(model.search("xyzunmatched"), [])
        self.assertEqual(model.search(""), [])
        self.assertEqual(model.search("特休", 0), [])
        self.assertEqual(BM25([]).search("anything"), [])

    def test_bm25_score_matches_hand_calculation(self):
        chunks = chunk_document(Document("a", "a", "apple apple")) + chunk_document(Document("b", "b", "banana"))
        score = BM25(chunks).search("apple")[0][1]
        expected = math.log(2) * 2 * 2.2 / (2 + 1.2 * (0.25 + 0.75 * 2 / 1.5))
        self.assertAlmostEqual(score, expected)

    def test_permission_filtering_before_context(self):
        hits = retrieve(self.chunks, "薪資設定", roles={"reader"})
        self.assertNotIn("salary", [c.doc_id for c, _ in hits])
        context, _ = pack_context(hits)
        self.assertNotIn("999999", context)
        self.assertEqual(retrieve(self.chunks, "薪資", roles={"hr"})[0][0].doc_id, "salary")

    def test_empty_roles_fail_closed(self):
        self.assertEqual(retrieve(self.chunks, "特休", roles=set()), [])

    def test_tenant_and_inactive_filtering(self):
        hits = retrieve(self.chunks, "出差住宿費")
        self.assertNotIn("travel-old", [c.doc_id for c, _ in hits])
        self.assertEqual(retrieve(self.chunks, "特休", tenant="other")[0][0].doc_id, "other")
        self.assertEqual(retrieve(self.chunks, "特休", tenant="missing"), [])

    def test_cosine_geometry_and_validation(self):
        self.assertAlmostEqual(cosine([1., 0.], [2., 0.]), 1)
        self.assertEqual(cosine([1., 0.], [0., 1.]), 0)
        self.assertEqual(cosine([0., 0.], [1., 1.]), 0)
        for a, b in [([], []), ([1], [1, 2]), ([math.nan], [1])]:
            with self.assertRaises(ValueError):
                cosine(a, b)

    def test_rrf_uses_rank_not_raw_score(self):
        a, b = self.chunks[:2]
        result = rrf([[(a, 999), (b, 1)], [(b, 0.9)]])
        self.assertEqual(result[0][0], b)
        self.assertAlmostEqual(result[0][1], 1 / 62 + 1 / 61)

    def test_rrf_duplicate_in_one_ranking_no_extra_vote(self):
        chunk = self.chunks[0]
        self.assertAlmostEqual(rrf([[(chunk, 2), (chunk, 1)]])[0][1], 1 / 61)
        with self.assertRaises(ValueError):
            rrf([], c=0)

    def test_context_budget_includes_labels_and_separators(self):
        hits = retrieve(self.chunks, "出差住宿")
        full, sources = pack_context(hits, 10000)
        exact, exact_sources = pack_context(hits, len(full))
        self.assertEqual(exact, full)
        self.assertEqual(exact_sources, sources)
        small, _ = pack_context(hits, 40)
        self.assertLessEqual(len(small), 40)
        with self.assertRaises(ValueError):
            pack_context(hits, -1)

    def test_empty_context_refuses(self):
        self.assertEqual(extractive_answer("特休", {})["status"], "insufficient_evidence")

    def test_answer_quotes_authorized_source(self):
        answer = ask("特休申請提前")
        self.assertEqual(answer["status"], "extractive_demo")
        self.assertIn("三個工作日", answer["answer"])
        self.assertEqual(answer["citations"][0]["doc_id"], "leave")
        self.assertIn(answer["citations"][0]["quote"], answer["context"])

    def test_unanswerable_query(self):
        self.assertEqual(ask("火星基地氧氣費率")['status'], "insufficient_evidence")

    def test_citation_existence_is_not_entailment(self):
        _, evidence = pack_context(retrieve(self.chunks, "特休"))
        self.assertTrue(validate_citations("錯誤事實仍可能通過編號檢查 [S1]", evidence))
        self.assertFalse(validate_citations("不存在 [S999]", evidence))
        self.assertFalse(validate_citations("完全沒引用", evidence))

    def test_metrics_hand_calculated(self):
        result = retrieval_metrics(["x", "a", "b"], {"a": 2, "b": 1}, 3)
        self.assertAlmostEqual(result['precision'], 2 / 3)
        self.assertEqual(result['recall'], 1)
        self.assertEqual(result['mrr'], 0.5)
        expected = (3 / math.log2(3) + 1 / math.log2(4)) / (3 + 1 / math.log2(3))
        self.assertAlmostEqual(result['ndcg'], expected)

    def test_metrics_duplicates_do_not_inflate_gain(self):
        result = retrieval_metrics(["a", "a"], {"a": 1, "b": 1}, 2)
        self.assertEqual(result['recall'], 0.5)
        self.assertEqual(result['precision'], 0.5)
        self.assertLess(result['ndcg'], 1)

    def test_metrics_empty_and_invalid(self):
        self.assertEqual(retrieval_metrics([], {}, 3)['ndcg'], 0)
        with self.assertRaises(ValueError):
            retrieval_metrics([], {}, 0)

    def test_incremental_update_changes_content_once(self):
        with sqlite3.connect(":memory:") as connection:
            doc = self.documents[0]
            self.assertTrue(upsert_document(connection, doc))
            self.assertFalse(upsert_document(connection, doc))
            changed = replace(doc, text="新的休假規範", version="2")
            self.assertTrue(upsert_document(connection, changed))
            self.assertEqual(read_store(connection, "demo"), [changed])

    def test_same_doc_id_can_exist_in_different_tenants(self):
        with sqlite3.connect(":memory:") as connection:
            doc = self.documents[0]
            upsert_document(connection, doc)
            other = replace(doc, tenant="other", text="不同內容")
            upsert_document(connection, other)
            self.assertEqual(read_store(connection, "demo"), [doc])
            self.assertEqual(read_store(connection, "other"), [other])

    def test_deletion_is_scoped_and_sql_is_parameterized(self):
        with sqlite3.connect(":memory:") as connection:
            doc = replace(self.documents[0], id="' OR 1=1 --")
            upsert_document(connection, doc)
            upsert_document(connection, self.documents[1])
            with connection:
                connection.execute("DELETE FROM documents WHERE tenant=? AND id=?", (doc.tenant, doc.id))
            self.assertEqual(len(read_store(connection, "demo")), 1)

    def test_cache_key_separates_permissions_and_versions(self):
        original = cache_key("特休", "demo", {"reader"}, "v1", "model-a")
        for scope in [("other", {"reader"}, "v1", "model-a"), ("demo", {"hr"}, "v1", "model-a"),
                      ("demo", {"reader"}, "v2", "model-a"), ("demo", {"reader"}, "v1", "model-b")]:
            self.assertNotEqual(original, cache_key("特休", *scope))

    @patch.object(provider_http, "post")
    def test_embedding_response_reorders_by_index(self, post):
        post.return_value = {"data": [{"index": 1, "embedding": [0., 1.]}, {"index": 0, "embedding": [1., 0.]}]}
        self.assertEqual(provider_http.embeddings(["a", "b"]), [[1., 0.], [0., 1.]])

    @patch.object(provider_http, "post")
    def test_embedding_response_rejects_wrong_shape(self, post):
        post.return_value = {"data": [{"index": 1, "embedding": [1.]}]}
        with self.assertRaises(ValueError):
            provider_http.embeddings(["a"])

    @patch.object(provider_http, "post")
    def test_responses_parses_text_items_and_checks_status(self, post):
        post.return_value = {"status": "completed", "output": [{"type": "reasoning"}, {"type": "message", "content": [{"type": "output_text", "text": "答案 [S1]"}]}]}
        self.assertEqual(provider_http.generate("q", "evidence", "example-model")['answer'], "答案 [S1]")
        post.return_value = {"status": "incomplete", "output": []}
        self.assertEqual(provider_http.generate("q", "evidence", "example-model")['status'], "incomplete")

    @patch.object(provider_http, "post")
    def test_empty_context_never_calls_api(self, post):
        self.assertEqual(provider_http.generate("q", "", "example-model")['status'], "insufficient_evidence")
        post.assert_not_called()

    def test_small_development_set_at_document_level(self):
        rows = json.loads((HERE / "data/qrels.json").read_text(encoding="utf-8"))
        for row in rows:
            ids = list(dict.fromkeys(c.doc_id for c, _ in retrieve(self.chunks, row['query'])))
            self.assertEqual(retrieval_metrics(ids, row['relevant'], 3)['recall'], 1)

    def test_all_entrypoints_default_offline_from_another_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            # A sitecustomize blocker makes accidental network I/O fail in each subprocess.
            blocker = Path(directory) / "sitecustomize.py"
            blocker.write_text("import socket\ndef blocked(*a,**k): raise RuntimeError('network forbidden in offline tests')\nsocket.create_connection=blocked\nsocket.socket.connect=blocked\n", encoding="utf-8")
            import os
            env = {**os.environ, "PYTHONUTF8": "1", "PYTHONPATH": directory}
            for path in sorted(HERE.glob("[0-9][0-9]_*.py")):
                process = subprocess.run([sys.executable, str(path.resolve())], cwd=directory,
                    env=env, capture_output=True, text=True, encoding="utf-8", timeout=15)
                self.assertEqual(process.returncode, 0, path.name + ": " + process.stderr)
                self.assertTrue(process.stdout.strip(), path.name)


if __name__ == "__main__":
    unittest.main()
