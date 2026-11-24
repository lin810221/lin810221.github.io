"""Numerical and full offline acceptance checks; no pretrained model access."""
import os
os.environ['HF_HUB_OFFLINE']='1'
os.environ['TOKENIZERS_PARALLELISM']='false'
import contextlib
import copy
import importlib.util
import io
import json
import math
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import torch
from torch.nn import functional as F
import lm_core as lm

HERE=Path(__file__).resolve().parent

def entry(name):
    spec=importlib.util.spec_from_file_location('tf_'+name.replace('.','_'),HERE/name)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

class TokenizerTests(unittest.TestCase):
    def test_unicode_roundtrip(self):
        tok=lm.ByteTokenizer()
        for text in ['','hello','學習🙂','e\u0301','é','<eos>']:
            self.assertEqual(tok.decode(tok.encode(text)),text)

    def test_codepoint_not_byte(self):
        text='學AI🙂'
        self.assertEqual(len(text),4);self.assertEqual(len(text.encode()),9)
        self.assertEqual(len(lm.ByteTokenizer().encode(text)),11)

    def test_byte_fragment_strict(self):
        tok=lm.ByteTokenizer();fragment=tok.encode('學',bos=False,eos=False)[:1]
        with self.assertRaises(UnicodeDecodeError):tok.decode(fragment)

    def test_literal_special_text_not_control(self):
        ids=lm.ByteTokenizer().encode('<eos>',bos=False,eos=False)
        self.assertNotIn(lm.ByteTokenizer.eos_id,ids)

    def test_bpe_unknown_unicode_lossless(self):
        tok=lm.TinyBPE().fit(['banana banana','bandana'],steps=12)
        for text in ['banana','新文字🙂','', 'e\u0301']:
            self.assertEqual(tok.decode(tok.encode(text)),text)

    def test_bpe_merges_reproducible(self):
        a=lm.TinyBPE().fit(['abab','baba'],8);b=lm.TinyBPE().fit(['abab','baba'],8)
        self.assertEqual(a.merges,b.merges);self.assertEqual(a.encode('abab'),b.encode('abab'))

    def test_overlapping_pair_merged_once_per_byte(self):
        self.assertEqual(lm.TinyBPE.merge([1,1,1],(1,1),256),[256,1])

    def test_bpe_not_refit_with_new_corpus(self):
        tok=lm.TinyBPE().fit(['abab'],1)
        with self.assertRaises(ValueError):tok.fit(['validation'],2)

    def test_library_local_tokenizer(self):
        tok=entry('03_local_tokenizer.py').build_tokenizer()
        self.assertEqual(tok.decode(tok.encode('未見文字🙂').ids),'未見文字🙂')


class AttentionTests(unittest.TestCase):
    def setUp(self):lm.seed_everything()

    def test_exact_rectangular_mask(self):
        self.assertEqual(lm.allowed_mask(2,5,3).int().tolist(),[[1,1,1,1,0],[1,1,1,1,1]])
        self.assertTrue(lm.allowed_mask(1,5,4).all())

    def test_square_mask(self):
        self.assertTrue(torch.equal(lm.allowed_mask(4,4),torch.ones(4,4,dtype=torch.bool).tril()))

    def test_reference_sdpa(self):
        q=torch.randn(2,3,2,4);k=torch.randn(2,3,5,4);v=torch.randn(2,3,5,6)
        mask=lm.allowed_mask(2,5,3)
        expected,weights=lm.reference_attention(q,k,v,mask)
        actual=F.scaled_dot_product_attention(q,k,v,attn_mask=mask,dropout_p=0.)
        torch.testing.assert_close(actual,expected)
        torch.testing.assert_close(weights.sum(-1),torch.ones_like(weights.sum(-1)))

    def test_no_allowed_key_is_explicit(self):
        with self.assertRaises(ValueError):lm.reference_attention(torch.ones(1,2),torch.ones(1,2),torch.ones(1,2),torch.zeros(1,1,dtype=torch.bool))

    def test_future_key_cannot_change_prefix(self):
        model=lm.TinyGPT().eval();a=torch.tensor([[1,10,11,12]]);b=a.clone();b[0,-1]=13
        with torch.inference_mode():torch.testing.assert_close(model(a)['logits'][:,:-1],model(b)['logits'][:,:-1])

    def test_rope_norm_and_relative_position(self):
        q=torch.randn(1,2,1,8,dtype=torch.float64);k=torch.randn_like(q)
        a=lm.rope(q,torch.tensor([3]));b=lm.rope(k,torch.tensor([7]))
        c=lm.rope(q,torch.tensor([13]));d=lm.rope(k,torch.tensor([17]))
        torch.testing.assert_close(a.norm(dim=-1),q.norm(dim=-1))
        torch.testing.assert_close((a*b).sum(-1),(c*d).sum(-1))

    def test_gqa_reference(self):
        q=torch.randn(1,4,3,8);k=torch.randn(1,2,3,8);v=torch.randn_like(k)
        a=F.scaled_dot_product_attention(q,k,v,is_causal=True,enable_gqa=True)
        b=F.scaled_dot_product_attention(q,k.repeat_interleave(2,1),v.repeat_interleave(2,1),is_causal=True)
        torch.testing.assert_close(a,b)

    def test_online_softmax_chunk_independent(self):
        algorithm=entry('21_online_softmax.py').online_weighted
        scores=torch.tensor([1000.,999.,1003.,998.],dtype=torch.float64);values=torch.arange(12,dtype=torch.float64).reshape(4,3)
        for chunk in [1,2,3,4]:torch.testing.assert_close(algorithm(scores,values,chunk),scores.softmax(-1)@values)


class LossAndDataTests(unittest.TestCase):
    def test_shift_once(self):
        x,y,m=lm.make_batch(['ab'])
        self.assertEqual(x.tolist(),[[1,100,101]])
        self.assertEqual(y.tolist(),[[100,101,2]])

    def test_padding_ignored(self):
        x,y,m=lm.make_batch(['a','ab'])
        self.assertEqual(y.tolist(),[[100,2,-100],[100,101,2]])
        loss,count=lm.language_loss(torch.zeros(2,3,259),y)
        self.assertEqual(count,5);self.assertAlmostEqual(float(loss),math.log(259),places=5)

    def test_ignored_logits_not_in_loss(self):
        x,y,m=lm.make_batch(['a','ab']);a=torch.zeros(2,3,259);b=a.clone();b[0,2]=torch.randn(259)*100
        self.assertEqual(float(lm.language_loss(a,y)[0]),float(lm.language_loss(b,y)[0]))

    def test_all_ignored_is_not_zero_loss(self):
        with self.assertRaises(ValueError):lm.language_loss(torch.zeros(1,2,5),torch.full((1,2),-100,dtype=torch.long))

    def test_corpus_sentence_disjoint(self):
        train,valid=lm.toy_corpus();self.assertEqual((len(train),len(valid)),(25,7));self.assertFalse(set(train)&set(valid))

    def test_gradient_accumulation_weights_tokens(self):
        lm.seed_everything();a=lm.TinyGPT();b=copy.deepcopy(a)
        x,y,m=lm.make_batch(['a','red bird moves.','fish.']);total=int((y!=-100).sum())
        lm.language_loss(a(x,attention_mask=m)['logits'],y)[0].backward()
        for i in range(len(x)):
            loss,count=lm.language_loss(b(x[i:i+1],attention_mask=m[i:i+1])['logits'],y[i:i+1]);(loss*count/total).backward()
        for p,q in zip(a.parameters(),b.parameters()):torch.testing.assert_close(p.grad,q.grad,atol=3e-6,rtol=1e-4)


class CacheTests(unittest.TestCase):
    def setUp(self):lm.seed_everything();self.model=lm.TinyGPT().eval();self.ids=torch.tensor([[1,10,11,12,13],[1,30,31,32,33]])

    def test_chunk_and_token_parity(self):
        with torch.inference_mode():
            full=self.model(self.ids)['logits']
            for split in [1,2,3,4]:
                prefix=self.model(self.ids[:,:split],use_cache=True)
                tail=self.model(self.ids[:,split:],cache=prefix['cache'],use_cache=True)
                torch.testing.assert_close(tail['logits'],full[:,split:],atol=1e-6,rtol=1e-5)
                self.assertEqual(tail['cache'][0][0].shape,(2,4,5,8))

    def test_incremental_all_positions(self):
        with torch.inference_mode():
            expected=self.model(self.ids)['logits'];cache=None;outputs=[]
            for i in range(5):
                out=self.model(self.ids[:,i:i+1],cache=cache,use_cache=True);cache=out['cache'];outputs.append(out['logits'])
            torch.testing.assert_close(torch.cat(outputs,1),expected,atol=1e-6,rtol=1e-5)

    def test_padding_position_parity(self):
        ids=self.ids[:,:4].clone();ids[0,3]=0;m=ids!=0
        with torch.inference_mode():
            prefix=self.model(ids,attention_mask=m,use_cache=True)
            out=self.model(torch.tensor([[99],[98]]),cache=prefix['cache'],attention_mask=torch.cat((m,torch.ones(2,1,dtype=torch.bool)),1))
            single=self.model(torch.tensor([[1,10,11,99]]))
            torch.testing.assert_close(out['logits'][0,-1],single['logits'][0,-1],atol=1e-6,rtol=1e-5)

    def test_context_exhaustion_explicit(self):
        with self.assertRaises(ValueError):self.model(torch.ones(1,65,dtype=torch.long))

    def test_wrong_mask_length_explicit(self):
        with self.assertRaises(ValueError):self.model(self.ids,attention_mask=torch.ones(2,1,dtype=torch.bool))

    def test_all_masked_query_explicit(self):
        with self.assertRaises(ValueError):self.model(self.ids,attention_mask=torch.zeros_like(self.ids))

    def test_damaged_layer_cache_rejected(self):
        with torch.inference_mode():cache=self.model(self.ids[:,:3],use_cache=True)['cache']
        cache[1]=(cache[1][0][:,:,:2],cache[1][1][:,:,:2])
        with self.assertRaises(ValueError):self.model(self.ids[:,3:4],cache=cache)

    def test_kv_capacity(self):
        self.assertEqual(lm.kv_bytes(2,32,4096,8,128,2),2**30)
        self.assertEqual(lm.kv_bytes(2,32,4096,32,128,2),4*2**30)


class GenerationTests(unittest.TestCase):
    def test_top_p_crossing_token_retained(self):
        result=lm.filter_logits(torch.log(torch.tensor([.6,.25,.1,.05])),top_p=.8).softmax(-1)
        torch.testing.assert_close(result,torch.tensor([.6/.85,.25/.85,0,0]))

    def test_top_k_exact_ties(self):
        result=lm.filter_logits(torch.zeros(5),top_k=2)
        self.assertEqual(torch.isfinite(result).tolist(),[True,True,False,False,False])

    def test_invalid_policy_rejected(self):
        for options in [{'temperature':0},{'top_p':0},{'top_k':0},{'top_k':4}]:
            with self.assertRaises(ValueError):lm.filter_logits(torch.zeros(3),**options)

    def test_greedy_cached_same_tokens(self):
        lm.seed_everything();model=lm.TinyGPT().eval();ids=torch.tensor([[1,30,31]])
        self.assertTrue(torch.equal(lm.generate(model,ids,8,False),lm.generate(model,ids,8,True)))

    def test_sampling_seed_reproducible(self):
        lm.seed_everything();model=lm.TinyGPT().eval();ids=torch.tensor([[1,30,31]])
        self.assertTrue(torch.equal(lm.generate(model,ids,8,sample=True,seed=7),lm.generate(model,ids,8,sample=True,seed=7)))

    def test_generation_eval_and_budget(self):
        model=lm.TinyGPT();ids=torch.tensor([[1,30]])
        with self.assertRaises(ValueError):lm.generate(model,ids)
        with self.assertRaises(ValueError):lm.generate(model.eval(),ids,max_new_tokens=70)
        self.assertTrue(torch.equal(lm.generate(model,ids,max_new_tokens=0),ids))


class TrainingAndArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.model,cls.report=lm.train_tiny()

    def test_training_loss_and_generator_holdout(self):
        self.assertLess(self.report['last_train_nll'],self.report['first_train_nll']*.2)
        self.assertLess(self.report['valid_nll'],1.5)
        self.assertEqual(self.report['valid_target_tokens'],129)

    def test_train_reproducible(self):
        model,report=lm.train_tiny();self.assertEqual(self.report,report)
        for a,b in zip(model.parameters(),self.model.parameters()):self.assertTrue(torch.equal(a,b))

    def test_tied_safetensors_roundtrip(self):
        with TemporaryDirectory() as folder:
            lm.save_artifact(self.model,folder,self.report);restored=lm.load_artifact(folder)
            x=torch.tensor([[1,100,101]])
            with torch.inference_mode():torch.testing.assert_close(self.model(x)['logits'],restored(x)['logits'])
            self.assertIs(restored.head.weight,restored.embedding.weight)
            self.assertTrue((Path(folder)/'loss.svg').is_file())

    def test_hash_tampering_rejected(self):
        with TemporaryDirectory() as folder:
            lm.save_artifact(self.model,folder);p=Path(folder)/'model.safetensors';p.write_bytes(p.read_bytes()+b'!')
            with self.assertRaises(ValueError):lm.load_artifact(folder)


class IntegrationTests(unittest.TestCase):
    def test_every_entrypoint_offline(self):
        # Stronger than HF offline flags: any socket connect fails this test.
        with (patch('socket.socket.connect',side_effect=AssertionError('No network in examples')),
              patch('socket.create_connection',side_effect=AssertionError('No network in examples')),
              patch('torch.hub.download_url_to_file',side_effect=AssertionError('No downloads'))):
            for path in sorted(HERE.glob('[0-9][0-9]_*.py')):
                with self.subTest(example=path.name),patch('sys.argv',[path.name]),contextlib.redirect_stdout(io.StringIO()) as output:
                    entry(path.name).main();self.assertTrue(output.getvalue().strip())

    def test_hf_cache_uses_current_API(self):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):entry('25_hf_cache.py').main()
        report=json.loads(output.getvalue());self.assertEqual(report['cache_length'],5)
        self.assertLess(report['max_logit_error'],1e-5)
        self.assertEqual(report['key_shape'],[1,2,5,8])

    def test_project_saved_deliverables(self):
        with TemporaryDirectory() as folder:
            with patch('sys.argv',['12_train_tiny_lm.py','--output',folder]),contextlib.redirect_stdout(io.StringIO()):entry('12_train_tiny_lm.py').main()
            for name in ['model.safetensors','config.json','tokenizer.json','manifest.json','report.json','loss.svg']:
                self.assertTrue((Path(folder)/name).is_file())


if __name__=='__main__':unittest.main()
