"""Meaningful numerical, fit/transform, adapter, and offline behavior checks."""
from dataclasses import replace
import json
import math
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import providers
from embedding_core import (EmbeddingSpec, Tfidf, binary_logit_loss, binary_metrics,
    cache_key, centroids, classify, cooccurrence, contrastive_loss, cosine, dequantize_int8,
    dot, euclidean, kmeans, mean_pool, nearest_neighbor_outlier_scores, norm, pca_2d,
    ppmi, quantize_int8, read_vector, retrieval_metrics, save_vector, search,
    silhouette, skipgram_step, tiny_skipgram, tokens, unit, vector, workbench)

HERE = Path(__file__).parent


class EmbeddingTests(unittest.TestCase):
    def test_vector_arithmetic_hand_calculation(self):
        self.assertEqual(dot([1, 2], [3, 4]), 11)
        self.assertEqual(norm([3, 4]), 5)
        self.assertEqual(euclidean([0, 0], [3, 4]), 5)
        self.assertAlmostEqual(cosine([1, 1], [2, 2]), 1)

    def test_cosine_invariant_to_positive_scale_and_rotation(self):
        a, b = [1., 2.], [3., -1.]
        rotate = lambda v: [-v[1], v[0]]
        self.assertAlmostEqual(cosine(a, b), cosine([10*x for x in a], b))
        self.assertAlmostEqual(cosine(a, b), cosine(rotate(a), rotate(b)))

    def test_invalid_vectors_are_rejected(self):
        for values in [[], [math.nan], [math.inf]]:
            with self.assertRaises(ValueError):
                vector(values)
        with self.assertRaises(ValueError):
            dot([1], [1, 2])
        with self.assertRaises(ValueError):
            cosine([0, 0], [1, 0])

    def test_unit_norm(self):
        self.assertAlmostEqual(norm(unit([3, 4])), 1)

    def test_tokenization_codes_and_chinese(self):
        self.assertIn("vpn-403", tokens("VPN-403"))
        self.assertIn("向量", tokens("向量相似度"))

    def test_tfidf_idf_matches_formula(self):
        model = Tfidf().fit(["apple fruit", "banana fruit"])
        self.assertAlmostEqual(model.idf[model.vocabulary.index('fruit')], 1)
        self.assertAlmostEqual(model.idf[model.vocabulary.index('apple')], math.log(3/2)+1)

    def test_tfidf_query_does_not_refit_or_add_vocabulary(self):
        model = Tfidf().fit(["apple fruit", "banana fruit"])
        before = (list(model.vocabulary), list(model.idf))
        self.assertEqual(norm(model.transform("unknownword")), 0)
        model.transform("apple unknownword")
        self.assertEqual((model.vocabulary, model.idf), before)

    def test_tfidf_refuses_empty_corpus(self):
        for corpus in [[], ["!!!"]]:
            with self.assertRaises(ValueError):
                Tfidf().fit(corpus)

    def test_exact_search_zero_and_ranking(self):
        self.assertEqual(search([0, 0], [[1, 0]]), [])
        self.assertEqual(search([1, 0], [[0, 1], [1, 0]])[0][0], 1)
        self.assertEqual(search([1, 0], [[1, 0]], 0), [])

    def test_cooccurrence_counts_are_symmetric(self):
        vocab, matrix = cooccurrence(['a', 'b', 'a'], 1)
        self.assertEqual(vocab, ['a', 'b'])
        self.assertEqual(matrix, [[0, 2], [2, 0]])

    def test_ppmi_hand_calculation(self):
        matrix = ppmi([[2, 0], [0, 2]])
        self.assertAlmostEqual(matrix[0][0], math.log(2))
        self.assertEqual(matrix[0][1], 0)
        self.assertEqual(ppmi([[0, 0], [0, 0]]), [[0, 0], [0, 0]])

    def test_stable_logit_loss(self):
        self.assertTrue(math.isfinite(binary_logit_loss(1000, 0)))
        self.assertTrue(math.isfinite(binary_logit_loss(-1000, 1)))
        self.assertAlmostEqual(binary_logit_loss(0, 1), math.log(2))

    def test_skipgram_update_matches_finite_difference_gradient(self):
        target, context = [.2, -.1], [.4, .3]
        epsilon, rate = 1e-6, .01
        original = target[:]
        def loss(x):
            return binary_logit_loss(dot(x, context), 1)
        for index in range(2):
            plus, minus = target[:], target[:]
            plus[index] += epsilon
            minus[index] -= epsilon
            gradient = (loss(plus)-loss(minus))/(2*epsilon)
            copied_target, copied_context = original[:], context[:]
            skipgram_step(copied_target, copied_context, 1, rate)
            self.assertAlmostEqual(copied_target[index], original[index]-rate*gradient, places=8)

    def test_tiny_training_is_real_and_deterministic(self):
        a, b = tiny_skipgram(), tiny_skipgram()
        self.assertEqual(a, b)
        self.assertLess(a['final_loss'], a['initial_loss']*.8)

    def test_contrastive_equal_scores_hand_calculation(self):
        loss, probabilities = contrastive_loss([0., 0., 0.], .1)
        self.assertAlmostEqual(loss, math.log(3))
        self.assertAlmostEqual(sum(probabilities), 1)
        self.assertAlmostEqual(probabilities[0], 1/3)

    def test_contrastive_temperature_with_wrong_positive(self):
        low, _ = contrastive_loss([.2, .9, .1], .05)
        high, _ = contrastive_loss([.2, .9, .1], 1.)
        self.assertGreater(low, high)
        with self.assertRaises(ValueError):
            contrastive_loss([1, 0], 0)

    def test_pooling_mask_changes_handmade_pad_direction(self):
        hidden = [[1, 0], [0, 1], [2, -1]]
        self.assertEqual(mean_pool(hidden, [1, 1, 0]), [.5, .5])
        self.assertEqual(mean_pool(hidden, [1, 1, 1]), [1, 0])
        with self.assertRaises(ValueError):
            mean_pool(hidden, [0, 0, 0])

    def test_pooling_shape_validation(self):
        with self.assertRaises(ValueError):
            mean_pool([[1], [1, 2]], [1, 1])

    def test_centroid_classifier(self):
        prototypes = centroids([[1, 0], [.9, .1], [0, 1]], ['a', 'a', 'b'])
        self.assertEqual(classify([1, 0], prototypes)[0], 'a')
        self.assertEqual(classify([0, 1], prototypes)[0], 'b')

    def test_kmeans_clusters_known_separated_points(self):
        points = [[0, 0], [0, 2], [10, 10], [10, 12]]
        centers, labels, inertia = kmeans(points, 2)
        self.assertEqual(labels[0], labels[1])
        self.assertEqual(labels[2], labels[3])
        self.assertNotEqual(labels[0], labels[2])
        self.assertAlmostEqual(inertia, 4)
        self.assertEqual(centers, [[0, 1], [10, 11]])

    def test_kmeans_validation(self):
        for points, k in [([], 1), ([[0, 0]], 2), ([[1, 1], [1, 1]], 2)]:
            with self.assertRaises(ValueError):
                kmeans(points, k)

    def test_silhouette_high_for_separated_groups(self):
        points = [[0, 0], [0, .1], [10, 10], [10, 10.1]]
        self.assertGreater(silhouette(points, [0, 0, 1, 1]), .98)
        with self.assertRaises(ValueError):
            silhouette(points, [0, 0, 0, 0])

    def test_threshold_metrics_hand_calculation(self):
        result = binary_metrics([1, 1, 0, 0], [.9, .4, .8, .1], .5)
        self.assertEqual((result['tp'],result['fp'],result['fn'],result['tn']), (1, 1, 1, 1))
        self.assertEqual(result['precision'], .5)
        self.assertEqual(result['recall'], .5)
        self.assertEqual(result['f1'], .5)

    def test_threshold_no_predicted_positives(self):
        result = binary_metrics([1, 0], [.9, .1], 1.)
        self.assertEqual(result['precision'], 0)
        self.assertEqual(result['recall'], 0)

    def test_isolated_point_has_largest_nearest_other_distance(self):
        scores = nearest_neighbor_outlier_scores([[0, 0], [.1, 0], [10, 10]])
        self.assertEqual(max(range(3), key=lambda i:scores[i]), 2)

    def test_retrieval_duplicate_ids_not_double_counted(self):
        result = retrieval_metrics(['a', 'a', 'x'], {'a', 'b'}, 3)
        self.assertEqual(result['recall'], .5)
        self.assertEqual(result['precision'], 1/3)
        self.assertEqual(result['mrr'], 1)

    def test_pca_centering_and_direction(self):
        result = pca_2d([[1, 1], [2, 2], [3, 3]])
        shifted = pca_2d([[11, -4], [12, -3], [13, -2]])
        self.assertEqual(result['mean'], [2, 2])
        self.assertAlmostEqual(result['explained_variance_ratio'], 1)
        self.assertAlmostEqual(result['component'][0], 1/math.sqrt(2))
        for a,b in zip(result['projected'], shifted['projected']):
            self.assertAlmostEqual(a,b)

    def test_pca_vertical_and_constant_points(self):
        self.assertEqual(pca_2d([[2, 0], [2, 1]])['component'], [0, 1])
        self.assertEqual(pca_2d([[1, 1], [1, 1]])['explained_variance_ratio'], 0)

    def test_quantization_error_bound(self):
        original = [.123, -.56, 1.1, 0]
        codes, scale = quantize_int8(original)
        restored = dequantize_int8(codes, scale)
        self.assertLessEqual(max(abs(a-b) for a,b in zip(original,restored)), scale/2+1e-12)
        self.assertTrue(all(-127<=code<=127 for code in codes))

    def test_zero_quantization_roundtrip(self):
        codes, scale = quantize_int8([0, 0])
        self.assertEqual(dequantize_int8(codes,scale), [0, 0])

    def test_manifest_separates_equal_dimension_models(self):
        a = EmbeddingSpec('test','model-a','v1',2,'q','d')
        b = replace(a, model='model-b')
        with sqlite3.connect(':memory:') as connection:
            save_vector(connection,'doc',[1,0],a)
            self.assertEqual(read_vector(connection,'doc',a),[1,0])
            self.assertIsNone(read_vector(connection,'doc',b))
            with self.assertRaises(ValueError):
                save_vector(connection,'wrong',[1,2,3],a)

    def test_cache_contract_distinguishes_role_and_version(self):
        spec = EmbeddingSpec('test','model','v1',2,'q','d')
        self.assertNotEqual(cache_key('hi',spec,'query'),cache_key('hi',spec,'document'))
        self.assertNotEqual(cache_key('hi',spec,'query'),cache_key('hi',replace(spec,revision='v2'),'query'))

    @patch.object(providers,'post')
    def test_openai_indices_not_return_order(self,post):
        post.return_value={'data':[{'index':1,'embedding':[0,1]},{'index':0,'embedding':[1,0]}]}
        self.assertEqual(providers.openai_embeddings(['a','b']),[[1,0],[0,1]])

    @patch.object(providers,'post')
    def test_openai_duplicate_index_rejected(self,post):
        post.return_value={'data':[{'index':0,'embedding':[1,0]},{'index':0,'embedding':[0,1]}]}
        with self.assertRaises(ValueError):
            providers.openai_embeddings(['a','b'])

    def test_gemini_config_uses_current_nested_schema(self):
        payload = providers.gemini_payload(['a'],'gemini-embedding-001','RETRIEVAL_QUERY',256)
        row = payload['requests'][0]
        self.assertNotIn('taskType',row)
        self.assertEqual(row['embedContentConfig'],{'taskType':'RETRIEVAL_QUERY','outputDimensionality':256})

    @patch.object(providers,'post')
    def test_gemini_batch_shape_and_order(self,post):
        post.return_value={'embeddings':[{'values':[1,0]},{'values':[0,1]}]}
        self.assertEqual(providers.gemini_embeddings(['a','b']),[[1,0],[0,1]])
        post.return_value={'embeddings':[{'values':[1]}]}
        with self.assertRaises(ValueError):
            providers.gemini_embeddings(['a','b'])

    def test_provider_payload_rejects_invalid_requests(self):
        with self.assertRaises(ValueError):
            providers.openai_payload([''])
        with self.assertRaises(ValueError):
            providers.gemini_payload(['a'],model='../bad')

    def test_workbench_known_and_oov_queries(self):
        result = workbench('向量 相似度 cosine')
        self.assertEqual(result['mode'],'offline_lexical_tfidf')
        self.assertEqual(result['hits'][0]['id'],'vectors')
        self.assertEqual(workbench('qwertyunseentoken')['hits'],[])

    def test_all_twenty_entrypoints_offline_from_another_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory,'sitecustomize.py').write_text("import socket\ndef blocked(*a,**k): raise RuntimeError('network forbidden')\nsocket.create_connection=blocked\nsocket.socket.connect=blocked\n",encoding='utf-8')
            env={**os.environ,'PYTHONPATH':directory,'PYTHONUTF8':'1'}
            paths=sorted(HERE.glob('[0-9][0-9]_*.py'))
            self.assertEqual(len(paths),20)
            for path in paths:
                result=subprocess.run([sys.executable,str(path.resolve())],cwd=directory,env=env,capture_output=True,text=True,encoding='utf-8',timeout=15)
                self.assertEqual(result.returncode,0,path.name+': '+result.stderr)
                self.assertTrue(result.stdout.strip(),path.name)


if __name__ == '__main__':
    unittest.main()
