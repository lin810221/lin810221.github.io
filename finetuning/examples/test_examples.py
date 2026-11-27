"""Behavioral contracts, real PEFT/TRL CPU training, no remote weights."""
import copy,json,math,unittest,uuid
from pathlib import Path
import torch
from finetune_core import *

class FineTuningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output=Path(__file__).resolve().parent/'outputs/tests'/uuid.uuid4().hex
        cls.output.mkdir(parents=True)

    def test_schema_rejects_invalid_rows(self):
        self.assertEqual(validate_rows(records()),12)
        for mutate in [lambda r:r.update(id=''),lambda r:r['messages'][-1].update(role='tool'),
                       lambda r:r['messages'][-1].update(content='')]:
            row=copy.deepcopy(records()[0]);mutate(row)
            with self.assertRaises(ValueError):validate_rows([row])
        with self.assertRaises(ValueError):validate_rows([records()[0],records()[0]])

    def test_group_split_and_content_duplicates_are_distinct(self):
        a,b=split_groups(records(),{'case-9','case-10','case-11'})
        self.assertFalse({r['group'] for r in a}&{r['group'] for r in b})
        self.assertEqual(len(duplicates(records())),3)
        self.assertTrue({content_hash(r) for r in a}&{content_hash(r) for r in b})

    def test_assistant_span_and_eos(self):
        tok=tokenizer();r=encode(records()[0],tok)
        self.assertEqual([x for x in r['labels'] if x!=-100],[tok.convert_tokens_to_ids('warm'),tok.eos_token_id])
        self.assertTrue(all(x==-100 for x in r['labels'][:5]))

    def test_padding_is_position_based(self):
        a=encode(records()[0]);b=copy.deepcopy(a)
        b['input_ids']+=[3];b['labels']+=[3];b['attention_mask']+=[1]
        out=collate([a,b]);self.assertEqual(out['labels'][0,-1].item(),-100)
        self.assertEqual(out['labels'][0,-2].item(),3)

    def test_truncation_does_not_silently_delete_targets(self):
        with self.assertRaises(ValueError):encode(records()[0],max_length=3)

    def test_shifted_loss_matches_hf(self):
        model=tiny_model();b=batch();out=model(**b)
        self.assertAlmostEqual(shifted_loss(out.logits,b['labels']).item(),out.loss.item(),6)
        with self.assertRaises(ValueError):shifted_loss(out.logits,torch.full_like(b['labels'],-100))

    def test_full_sft_learns_small_batch(self):
        r=run(6,self.output/'full')
        self.assertLess(r['after']['nll'],r['before']['nll']*.5)

    def test_lora_initialization_and_first_gradient(self):
        r=lora_matrix_demo();self.assertEqual(r['delta_norm'],0)
        self.assertEqual(r['A_grad'],0);self.assertGreater(r['B_grad'],0)

    def test_real_peft_freezes_base_and_changes_adapter(self):
        base=tiny_model();before=copy.deepcopy(base.state_dict());model=lora(base);train(model,batch(),3)
        for name,tensor in before.items():
            # PEFT inserts base_layer under wrapped projections.
            key='base_model.model.'+name
            if '.q_proj.' in key or '.v_proj.' in key:key=key.replace('.weight','.base_layer.weight')
            self.assertTrue(torch.equal(tensor,model.state_dict()[key]),name)
        self.assertTrue(any(p.abs().sum()>0 for n,p in model.named_parameters() if 'lora_B' in n))
        self.assertLess(count_parameters(model)['trainable'],count_parameters(model)['all'])

    def test_rank_scaling(self):
        a=run(9,self.output/'rank')
        self.assertEqual(a['rank_4']['lora_scale'],2)
        self.assertEqual(a['rank_4']['rslora_scale'],4)
        self.assertEqual(a['rank_8']['counts']['trainable'],2*a['rank_4']['counts']['trainable'])

    def test_uniform_quantization_and_resource_assumptions(self):
        r=quantize_toy([0.,.2,1.]);self.assertGreaterEqual(r['mse'],0)
        m=memory_bytes(7_000_000_000,8_000_000)
        self.assertEqual(m['base'],3_500_000_000);self.assertEqual(m['trainable_weights_grad_adam'],128_000_000)
        self.assertFalse(qlora_recipe()['executed_gpu_training'])

    def test_unequal_microbatches_match_concatenated_gradient(self):
        self.assertLess(accumulation_error(),1e-6)

    def test_exact_optimizer_boundary_resume(self):
        self.assertEqual(resume_demo(self.output/'resume'),0.)

    def test_sequence_scores_exclude_prompt_and_sum_targets(self):
        seed();m=tiny_model();b=batch();scores=sequence_logps(m,b)
        self.assertAlmostEqual(-scores.sum().item()/(b['labels'][:,1:]!=-100).sum().item(),m(**b).loss.item(),5)

    def test_dpo_direction_reference_detach_and_baseline(self):
        p=torch.tensor([1.],requires_grad=True);ref=torch.tensor([1.],requires_grad=True);zero=torch.zeros(1)
        loss=dpo_loss(p,zero,ref,zero,.2);self.assertAlmostEqual(loss.item(),math.log(2),6)
        loss.backward();self.assertLess(p.grad.item(),0);self.assertIsNone(ref.grad)
        self.assertLess(dpo_loss(torch.tensor([3.]),zero,ref,zero).item(),loss.item())

    def test_distillation_teacher_is_fixed(self):
        s=torch.randn(2,5,requires_grad=True);t=torch.randn(2,5,requires_grad=True)
        distillation(s,t).backward();self.assertIsNone(t.grad);self.assertIsNotNone(s.grad)
        with self.assertRaises(ValueError):distillation(s,t[:,:3])

    def test_adapter_reload_and_merge_numerics(self):
        r=artifact_demo(self.output/'artifact')
        self.assertLess(r['reload_max_abs'],1e-6);self.assertLess(r['merge_max_abs'],2e-6)
        self.assertEqual(len(r['manifest']['base_sha256']),64)
        other=tiny_model();next(other.parameters()).data.add_(1)
        self.assertNotEqual(state_hash(other.state_dict()),r['manifest']['base_sha256'])
        with self.assertRaisesRegex(ValueError,'base identity'):load_verified_adapter(other,self.output/'artifact',tokenizer())
        tok=tokenizer();tok.chat_template+=' '
        with self.assertRaisesRegex(ValueError,'tokenizer'):load_verified_adapter(tiny_model(),self.output/'artifact',tok)

    def test_real_trl_sft_current_api(self):
        result=trl_sft(self.output/'trl-sft');self.assertEqual(result['steps'],2)
        self.assertTrue(math.isfinite(result['training_loss']))

    def test_real_trl_dpo_reference_frozen(self):
        result=trl_dpo(self.output/'trl-dpo');self.assertEqual(result['steps'],1)
        self.assertFalse(result['reference_requires_grad']);self.assertTrue(result['reference_unchanged'])
        self.assertAlmostEqual(result['training_loss'],math.log(2),5)

    def test_job_state_contract_and_capstone(self):
        self.assertEqual(job_trace(['validating','running','succeeded']),'succeeded')
        with self.assertRaises(ValueError):job_trace(['succeeded'])
        with self.assertRaises(ValueError):job_trace(['validating','running','failed','running'])
        r=run(24,self.output/'capstone')
        saved=json.loads((self.output/'capstone/report.json').read_text(encoding='utf-8'))
        self.assertEqual(r,saved);self.assertTrue(r['synthetic'])

    def test_all_24_entrypoints(self):
        # Reuses one interpreter: verifies every entry function without slow subprocess imports.
        for n in range(1,25):
            with self.subTest(example=n):self.assertIsInstance(run(n,self.output/f'entry-{n}'),dict)

    def test_local_model_route_and_leakage_guard(self):
        import sys
        from unittest.mock import patch
        from train_local import main,validate_splits
        rows=records()[:3]
        with self.assertRaises(ValueError):validate_splits(rows,rows)
        valid=copy.deepcopy(rows)
        for r in valid:
            r['id']='valid-'+r['id'];r['group']='valid-'+r['group']
            r['messages'][0]['content']='answer '+r['messages'][0]['content']
        validate_splits(rows,valid)
        root=self.output/'local-route';base=root/'base';base.mkdir(parents=True)
        tiny_model().save_pretrained(base);tokenizer().save_pretrained(base)
        for name,data in [('train',rows),('valid',valid)]:
            (root/f'{name}.jsonl').write_text('\n'.join(json.dumps(x) for x in data),encoding='utf-8')
        with patch.object(sys,'argv',['train_local.py','--model',str(base),'--train',str(root/'train.jsonl'),
            '--valid',str(root/'valid.jsonl'),'--output',str(root/'result'),'--cpu','--steps','2']):main()
        manifest=json.loads((root/'result/manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['method'],'lora')
        self.assertTrue((root/'result/model/adapter_model.safetensors').is_file())
        self.assertIn('model.safetensors',manifest['base_files'])

if __name__=='__main__':unittest.main()
