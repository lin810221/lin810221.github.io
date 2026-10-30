"""Numerical proofs and CPU integration tests for the original deep-learning examples."""
import contextlib,copy,importlib.util,io,json,math,os
from pathlib import Path
import socket,tempfile,unittest
from unittest.mock import patch
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader,TensorDataset
import course_core as c
ROOT=Path(__file__).resolve().parent

def entry(number):
    path=next(ROOT.glob(f'{number:02d}_*.py'));spec=importlib.util.spec_from_file_location(f'dl_{number}',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def run(number):
    with contextlib.redirect_stdout(io.StringIO()):return entry(number).main([])

class MathTests(unittest.TestCase):
    def setUp(self):c.setup()
    def test_framework_version(self):self.assertEqual(torch.__version__.split('+')[0],'2.15.0')
    def test_scalar_chain_matches_autograd(self):self.assertLess(run(3)['maximum_gradient_error'],1e-12)
    def test_matrix_chain_matches_autograd(self):self.assertLess(run(4)['maximum_error'],1e-12)
    def test_numerical_gradcheck(self):self.assertTrue(run(5)['gradcheck'])
    def test_softmax_crossentropy_derivative(self):self.assertLess(run(8)['maximum_gradient_error'],1e-7)
    def test_regression_losses_hand_calculation(self):
        result=run(7)
        self.assertAlmostEqual(result['mse']['loss'],5/3,places=6)
        self.assertEqual(result['mae']['loss'],1.)
        self.assertAlmostEqual(result['huber']['loss'],2/3,places=6)
    def test_activation_derivatives_at_zero(self):
        result=run(6)
        self.assertEqual(result['sigmoid']['derivatives'][2],.25)
        self.assertEqual(result['relu']['derivatives'][2],0)
        self.assertEqual(result['gelu']['derivatives'][2],.5)
    def test_receptive_field_matches_input_gradient(self):
        result=run(22);self.assertEqual(result['formula']['field'],9);self.assertEqual(result['actual_width'],9)
    def test_crosscorrelation_hand_result(self):
        result=run(21);self.assertEqual(result['output'][0][0],[[-4.,-4.],[-4.,-4.]])
    def test_xor_training_sanity(self):
        result=run(2);self.assertEqual(result['predictions'],[[0],[1],[1],[0]])
        self.assertLess(result['final_bce'],result['initial_bce']*.1)

class OptimizationTests(unittest.TestCase):
    def setUp(self):c.setup()
    def test_adamw_decoupled_decay(self):self.assertAlmostEqual(run(12)['AdamW']['weight_after_zero_data_gradient'],1.96,places=6)
    def test_momentum_second_update(self):self.assertAlmostEqual(run(11)['0.9'][1]['weight_after_step'],.46,places=6)
    def test_scheduler_update_order(self):self.assertEqual([r['lr_used'] for r in run(13)['trace']],[.1,.1,.05,.05,.025])
    def test_he_second_moment(self):
        result=run(14);self.assertLess(abs(result['relu_second_moment']-1),.15)
        self.assertLess(result['relu_centered_variance'],result['relu_second_moment'])
    def test_scalar_depth_product(self):
        result=run(15)
        for factor in (.5,1.,1.5):self.assertAlmostEqual(result[str(factor)]['derivative'],factor**20)
    def test_clipping_norm(self):
        result=run(16);self.assertEqual(result['pre_clip_norm'],5.)
        torch.testing.assert_close(torch.tensor(result['clipped_gradient']),torch.tensor([.6,.8]),atol=1e-6,rtol=1e-6)
    def test_weighted_accumulation_tail(self):self.assertLess(run(16)['maximum_update_difference'],1e-7)
    def test_dropout_scaling_and_eval(self):
        result=run(17);self.assertEqual(result['training_unique_values'],[0.,2.]);self.assertTrue(result['evaluation_is_identity'])
        self.assertLess(abs(result['training_mean']-1.),.05)
    def test_batchnorm_running_buffers(self):
        result=run(18)
        torch.testing.assert_close(torch.tensor(result['running_mean']),torch.tensor([.2,.3]))
        torch.testing.assert_close(torch.tensor(result['running_variance']),torch.tensor([1.1,1.1]))
    def test_layernorm_batch_independence(self):self.assertEqual(run(19)['layernorm_batch_independence_error'],0.)

class SequenceAttentionTests(unittest.TestCase):
    def setUp(self):c.setup()
    def test_variable_length_collate(self):
        tokens,lengths,labels=c.collate_tokens([([1,2],0),([3],1)])
        self.assertEqual(tokens.tolist(),[[1,2],[3,0]]);self.assertEqual(lengths.tolist(),[2,1]);self.assertEqual(labels.dtype,torch.long)
    def test_empty_sequence_rejected(self):
        with self.assertRaises(ValueError):c.collate_tokens([([],0)])
    def test_reserved_pad_rejected_in_raw_sequence(self):
        with self.assertRaises(ValueError):c.collate_tokens([([1,0],0)])
    def test_packed_sequence_ignores_extra_padding(self):
        model=c.SequenceModel().eval();lengths=torch.tensor([2])
        torch.testing.assert_close(model(torch.tensor([[1,2]]),lengths),model(torch.tensor([[1,2,0,0]]),lengths))
    def test_manual_rnn_unroll(self):self.assertLess(run(26)['manual_unroll_maximum_error'],1e-6)
    def test_gated_state_contracts(self):
        result=run(27);self.assertEqual(result['LSTM']['state_shapes'],[[1,2,4],[1,2,4]])
        self.assertTrue(result['GRU']['finite_gradients'])
    def test_manual_attention(self):
        result=run(30);self.assertLess(result['maximum_error'],1e-12)
        torch.testing.assert_close(torch.tensor(result['row_sums']),torch.ones(1,1,3))
    def test_causal_mask_prevents_future_value_leakage(self):
        result=run(31);self.assertEqual(result['early_positions_maximum_change'],0.)
        self.assertLess(result['mask_vs_is_causal_error'],1e-6)
    def test_block_causality_with_residuals(self):self.assertEqual(run(32)['early_positions_maximum_change'],0.)
    def test_contrastive_uniform_loss_and_gradients(self):
        result=run(33);self.assertAlmostEqual(result['collapsed_equal_logits_loss'],math.log(4),places=6)
        self.assertGreater(result['first_view_gradient_norm'],0)
        with self.assertRaises(ValueError):c.contrastive_loss(torch.zeros(3,2),torch.ones(3,2))

class GenerativeTests(unittest.TestCase):
    def setUp(self):c.setup()
    def test_kl_zero_for_standard_normal(self):self.assertEqual(c.kl_standard_normal(torch.zeros(2,3),torch.zeros(2,3)).sum().item(),0)
    def test_kl_known_mean(self):self.assertEqual(c.kl_standard_normal(torch.tensor([[1.,2.]]),torch.zeros(1,2)).item(),2.5)
    def test_reparameterization_gradients(self):
        model=c.TinyVAE();x=torch.randn(5,2);reconstruction,mean,logvar=model(x)
        loss=F.mse_loss(reconstruction,x)+c.kl_standard_normal(mean,logvar).mean();loss.backward()
        self.assertTrue(all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters()))
    def test_autoencoder_reconstruction_decreases(self):
        result=run(34);self.assertLess(result['final_mse'],result['initial_mse']*.5)
    def test_vae_mean_decode_improves(self):
        result=run(35);self.assertLess(result['final_mean_decode_mse'],result['initial_mean_decode_mse'])
        self.assertGreaterEqual(result['last_kl'],0)
    def test_discriminator_step_does_not_update_generator(self):
        g=nn.Linear(2,2);d=nn.Linear(2,1);before=c.snapshot(g)
        c.gan_discriminator_step(g,d,torch.optim.SGD(d.parameters(),lr=.1),torch.randn(4,2),torch.randn(4,2))
        self.assertTrue(all(torch.equal(before[k],v) for k,v in g.state_dict().items()))
        self.assertTrue(all(p.grad is None for p in g.parameters()))
    def test_generator_step_does_not_update_discriminator(self):
        g=nn.Linear(2,2);d=nn.Linear(2,1);before=c.snapshot(d)
        c.gan_generator_step(g,d,torch.optim.SGD(g.parameters(),lr=.1),torch.randn(4,2))
        self.assertTrue(all(torch.equal(before[k],v) for k,v in d.state_dict().items()))
        self.assertTrue(all(p.requires_grad for p in d.parameters()))
    def test_diffusion_schedule_posterior(self):
        beta,alpha,bar,variance=c.noise_schedule()
        self.assertTrue(torch.all(bar[1:]<bar[:-1]));self.assertEqual(variance[0].item(),0)
        self.assertTrue(torch.all(variance>=0));self.assertTrue(torch.allclose(bar,alpha.cumprod(0)))
    def test_forward_noising_closed_form(self):
        clean=torch.tensor([[2.],[3.]]);epsilon=torch.ones_like(clean);indices=torch.tensor([0,1]);bar=torch.tensor([.25,.81])
        actual=c.q_sample(clean,indices,epsilon,bar)
        expected=bar[:,None].sqrt()*clean+(1-bar[:,None]).sqrt()*epsilon
        torch.testing.assert_close(actual,expected)
    def test_actual_diffusion_training_and_sampling(self):
        result=run(37);self.assertLess(result['final_probe_mse'],result['initial_probe_mse'])
        self.assertTrue(math.isfinite(result['sample_std']))
    def test_flow_path_endpoints_and_velocity(self):
        z=torch.tensor([[1.],[2.]]);target=torch.tensor([[3.],[0.]])
        for t,expected in [(0.,z),(1.,target)]:
            x,v=c.flow_path(z,target,torch.full((2,1),t));torch.testing.assert_close(x,expected);torch.testing.assert_close(v,target-z)
    def test_actual_flow_training_and_integration(self):
        result=run(38);self.assertTrue(math.isfinite(result['last_velocity_mse']))
        self.assertTrue(math.isfinite(result['sample_std']))
    def test_teacher_is_detached_during_distillation(self):
        student=torch.randn(4,2,requires_grad=True);teacher=torch.randn(4,2,requires_grad=True)
        c.distillation_loss(student,teacher,torch.tensor([0,1,0,1])).backward()
        self.assertIsNone(teacher.grad);self.assertIsNotNone(student.grad)
    def test_identical_soft_targets_have_zero_kl(self):
        logits=torch.tensor([[1.,2.],[3.,-1.]])
        self.assertAlmostEqual(c.distillation_loss(logits,logits,torch.tensor([0,1]),hard_weight=0).item(),0.,places=6)

class ProjectTests(unittest.TestCase):
    def setUp(self):c.setup()
    def test_split_and_train_only_scaler(self):
        splits,_=c.make_data();self.assertEqual([len(s) for s in splits],[288,96,96])
        torch.testing.assert_close(splits[0].tensors[0].mean(0),torch.zeros(4),atol=1e-6,rtol=0)
        rows=[set(map(tuple,s.tensors[0].tolist())) for s in splits]
        self.assertFalse(rows[0]&rows[1] or rows[0]&rows[2] or rows[1]&rows[2])
    def test_validation_tail_weighting(self):
        model=nn.Linear(4,2);x=torch.randn(10,4);y=torch.arange(10)%2
        expected=F.cross_entropy(model(x),y).item()
        actual=c.evaluate(model,DataLoader(TensorDataset(x,y),batch_size=4))
        self.assertAlmostEqual(actual['loss'],expected,places=6);self.assertEqual(actual['samples'],10)
    def test_eval_restores_mode_and_no_gradients(self):
        model=c.MLP();loaders,_=c.make_loaders()
        c.evaluate(model,loaders[1]);self.assertTrue(model.training)
        self.assertTrue(all(p.grad is None for p in model.parameters()))
    def test_tabular_learning(self):
        result=c.experiment('tabular',epochs=8)
        self.assertLess(result['best_validation']['loss'],result['initial_validation']['loss']*.65)
    def test_cnn_learning(self):
        result=c.experiment('image')
        self.assertLess(result['best_validation']['loss'],result['initial_validation']['loss']*.5)
    def test_sequence_learning(self):
        result=c.experiment('sequence')
        self.assertLess(result['best_validation']['loss'],result['initial_validation']['loss']*.5)
    def test_snapshot_not_a_live_reference(self):
        model=nn.Linear(2,2);before=c.snapshot(model);saved=before['weight'].clone()
        with torch.no_grad():model.weight.add_(10)
        torch.testing.assert_close(before['weight'],saved)
    def test_checkpoint_roundtrip_and_no_overwrite(self):
        payload=c.experiment('tabular',epochs=2)['artifact']
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'model.pt';c.save_artifact(path,payload);loaded=c.load_artifact(path)
            self.assertEqual(c.predict_tabular(payload,c.prediction_rows()),c.predict_tabular(loaded,c.prediction_rows()))
            with self.assertRaises(FileExistsError):c.save_artifact(path,payload)
    def test_bad_raw_input_rejected(self):
        payload=c.experiment('tabular',epochs=1)['artifact']
        for rows in ([[1.,2.]],[[1.,2.,3.,float('nan')]],[]):
            with self.assertRaises(ValueError):c.predict_tabular(payload,rows)
    def test_unknown_checkpoint_format_and_version(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'bad.pt';torch.save({'format_version':9},path)
            with self.assertRaises(ValueError):c.load_artifact(path)
            torch.save({'format_version':1,'torch_version':'old'},path)
            with self.assertRaises(ValueError):c.load_artifact(path)
    def test_all_42_defaults_offline_from_other_cwd(self):
        previous=Path.cwd()
        def denied(*args,**kwargs):raise AssertionError('Default examples must remain offline')
        with tempfile.TemporaryDirectory() as folder:
            try:
                os.chdir(folder)
                with patch.object(socket.socket,'connect',denied),patch.object(socket,'create_connection',denied):
                    for number in range(1,43):
                        with self.subTest(example=number),contextlib.redirect_stdout(io.StringIO()) as output:
                            result=entry(number).main([]);self.assertEqual(result,json.loads(output.getvalue()))
            finally:os.chdir(previous)

if __name__=='__main__':unittest.main()
