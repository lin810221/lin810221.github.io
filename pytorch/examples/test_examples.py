"""Numerical and integration tests. CPU only; no datasets or models downloaded."""
import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, DistributedSampler
import course_core as c

ROOT = Path(__file__).parent


def entry(number):
    path = next(ROOT.glob(f"{number:02d}_*.py"))
    spec = importlib.util.spec_from_file_location(f"pytorch_example_{number}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TensorTests(unittest.TestCase):
    def setUp(self):
        c.setup()

    def test_tensor_matmul(self):
        x = torch.tensor([[1., 2.], [3., 4.]])
        torch.testing.assert_close(x @ torch.ones(2, 1), torch.tensor([[3.], [7.]]))

    def test_unintended_broadcast(self):
        self.assertEqual((torch.ones(4, 1) - torch.ones(4)).shape, (4, 4))
        self.assertEqual((torch.ones(4, 1) - torch.ones(4).unsqueeze(1)).shape, (4, 1))

    def test_keepdim(self):
        self.assertEqual(torch.ones(3, 4).mean(1, keepdim=True).shape, (3, 1))

    def test_view_strides(self):
        x = torch.arange(12).reshape(3, 4).t()
        self.assertFalse(x.is_contiguous())
        with self.assertRaises(RuntimeError):
            x.view(-1)
        torch.testing.assert_close(x.reshape(-1), x.contiguous().view(-1))

    def test_detach_shares_clone_independent(self):
        x = torch.tensor([1.], requires_grad=True)
        detached, cloned = x.detach(), x.detach().clone()
        detached.add_(2)
        self.assertEqual(x.item(), 3)
        self.assertEqual(cloned.item(), 1)

    def test_analytic_and_accumulated_grad(self):
        w = torch.tensor(2., requires_grad=True)
        ((3 * w - 10) ** 2).backward()
        self.assertEqual(w.grad.item(), -24)
        ((3 * w - 10) ** 2).backward()
        self.assertEqual(w.grad.item(), -48)

    def test_gradcheck_double(self):
        x = torch.tensor([.2, -.4], dtype=torch.double, requires_grad=True)
        self.assertTrue(torch.autograd.gradcheck(lambda v: (v.sin() * v).sum(), (x,)))

    def test_graph_freed(self):
        x = torch.tensor(2., requires_grad=True)
        loss = x * x
        loss.backward()
        with self.assertRaises(RuntimeError):
            loss.backward()

    def test_zero_grad_and_update(self):
        m = nn.Linear(1, 1, bias=False)
        opt = torch.optim.SGD(m.parameters(), lr=.1)
        before = m.weight.detach().clone()
        m(torch.ones(1, 1)).sum().backward()
        opt.step()
        torch.testing.assert_close(m.weight, before - .1)
        opt.zero_grad(set_to_none=True)
        self.assertIsNone(m.weight.grad)


class DataTests(unittest.TestCase):
    def test_invalid_dataset_contracts(self):
        for x, y in [(torch.ones(2), torch.zeros(2, dtype=torch.long)),
                     (torch.ones(2, 4), torch.zeros(2)),
                     (torch.full((2, 4), float('nan')), torch.zeros(2, dtype=torch.long))]:
            with self.subTest(shape=x.shape), self.assertRaises(ValueError):
                c.FeatureDataset(x, y)

    def test_splits_and_train_scaling(self):
        splits, prep = c.make_data()
        self.assertEqual([len(s) for s in splits], [96, 32, 32])
        torch.testing.assert_close(splits[0].x.mean(0), torch.zeros(4), atol=1e-6, rtol=0)
        torch.testing.assert_close(splits[0].x.std(0, unbiased=False), torch.ones(4))
        rows = [set(tuple(row) for row in s.x.tolist()) for s in splits]
        self.assertFalse(rows[0] & rows[1] or rows[0] & rows[2] or rows[1] & rows[2])
        # Independently reconstruct the raw train rows and scaler.
        cfg = c.Config()
        g = torch.Generator().manual_seed(cfg.seed + 100)
        raw = torch.randn(160, 4, generator=g)
        torch.randn(4, 3, generator=g)
        order = torch.randperm(160, generator=g)
        torch.testing.assert_close(prep['mean'], raw[order[:96]].mean(0))
        torch.testing.assert_close(splits[1].x, (raw[order[96:128]] - prep['mean']) / prep['scale'])

    def test_tail_batch(self):
        data = c.custom_dataset()
        self.assertEqual([len(y) for _, y in DataLoader(data, batch_size=4)], [4, 2])
        self.assertEqual([len(y) for _, y in DataLoader(data, batch_size=4, drop_last=True)], [4])

    def test_loader_reproducibility(self):
        a, _, _ = c.make_loaders()
        b, _, _ = c.make_loaders()
        torch.testing.assert_close(next(iter(a[0]))[0], next(iter(b[0]))[0])

    def test_collate_padding_and_mask(self):
        tokens, mask, labels = c.collate_sequences([([1, 2], 0), ([3], 1)])
        self.assertEqual(tokens.tolist(), [[1, 2], [3, 0]])
        self.assertEqual(mask.tolist(), [[True, True], [True, False]])
        self.assertEqual(labels.dtype, torch.long)

    def test_empty_sequence_rejected(self):
        with self.assertRaises(ValueError):
            c.collate_sequences([([], 0)])

    def test_pad_invariance_and_gradient(self):
        c.setup()
        model = c.SequenceClassifier()
        one = torch.tensor([[1, 2]])
        padded = torch.tensor([[1, 2, 0, 0]])
        torch.testing.assert_close(model(one, one.ne(0)), model(padded, padded.ne(0)))
        model(padded, padded.ne(0)).sum().backward()
        torch.testing.assert_close(model.embedding.weight.grad[0], torch.zeros(4))

    def test_all_masked_rejected(self):
        with self.assertRaises(ValueError):
            c.SequenceClassifier()(torch.zeros(1, 2, dtype=torch.long), torch.zeros(1, 2, dtype=torch.bool))

    def test_distributed_sampler_without_padding(self):
        ds = list(range(16))
        parts = [set(DistributedSampler(ds, num_replicas=2, rank=r, shuffle=False)) for r in range(2)]
        self.assertFalse(parts[0] & parts[1])
        self.assertEqual(parts[0] | parts[1], set(ds))

    def test_sampler_changes_epoch(self):
        sampler = DistributedSampler(list(range(32)), num_replicas=2, rank=0, seed=7)
        first = list(sampler)
        sampler.set_epoch(1)
        self.assertNotEqual(first, list(sampler))


class TrainingTests(unittest.TestCase):
    def setUp(self):
        c.setup()

    def test_module_registration(self):
        m = entry(7).CenteredMLP()
        self.assertIn('center', m.state_dict())
        self.assertGreater(len(list(m.parameters())), 0)
        self.assertEqual(len(list(entry(7).UnregisteredExample().parameters())), 0)

    def test_cross_entropy_contract(self):
        logits = torch.tensor([[2., 0., -1.], [0., 2., -1.]])
        labels = torch.tensor([0, 1])
        expected = -F.log_softmax(logits, 1)[torch.arange(2), labels].mean()
        torch.testing.assert_close(F.cross_entropy(logits, labels), expected)
        with self.assertRaises(RuntimeError):
            F.cross_entropy(logits, labels.float())

    def test_validation_weighted_tail(self):
        ds = c.custom_dataset()
        model = nn.Linear(4, 3)
        expected = F.cross_entropy(model(ds.x), ds.y).item()
        result = c.evaluate(model, DataLoader(ds, batch_size=4))
        self.assertAlmostEqual(result['loss'], expected, places=6)
        self.assertEqual(result['samples'], 6)

    def test_validation_preserves_training_mode(self):
        model = c.TinyMLP()
        loaders, _, _ = c.make_loaders()
        for mode in (True, False):
            model.train(mode)
            c.evaluate(model, loaders[1])
            self.assertEqual(model.training, mode)
            self.assertTrue(all(p.grad is None for p in model.parameters()))

    def test_eval_does_not_disable_autograd(self):
        model = nn.Linear(2, 1).eval()
        self.assertTrue(model(torch.ones(1, 2)).requires_grad)
        with torch.inference_mode():
            self.assertFalse(model(torch.ones(1, 2)).requires_grad)

    def test_loss_decreases_on_synthetic_data(self):
        result = c.experiment(c.Config(epochs=6))
        self.assertLess(result['final_validation']['loss'], result['initial_validation']['loss'] * .6)
        self.assertEqual(result['test']['samples'], 32)

    def test_partial_run_does_not_touch_test(self):
        self.assertIsNone(c.experiment(c.Config(epochs=4), stop_after=2)['test'])

    def test_state_snapshot_is_not_live_reference(self):
        model = nn.Linear(2, 1)
        snapshot = c.frozen_state(model)
        original = snapshot['weight'].clone()
        with torch.no_grad():
            model.weight.add_(10)
        torch.testing.assert_close(snapshot['weight'], original)

    def test_unequal_microbatch_accumulation(self):
        model = nn.Linear(4, 3)
        other = copy.deepcopy(model)
        x, y = torch.randn(10, 4), torch.arange(10) % 3
        a, b = torch.optim.SGD(model.parameters(), lr=.1), torch.optim.SGD(other.parameters(), lr=.1)
        F.cross_entropy(model(x), y).backward()
        a.step()
        c.accumulated_step(other, b, [(x[:4], y[:4]), (x[4:8], y[4:8]), (x[8:], y[8:])])
        for left, right in zip(model.parameters(), other.parameters()):
            torch.testing.assert_close(left, right, atol=1e-7, rtol=1e-6)

    def test_cpu_amp_fallback_matches_fp32(self):
        model, x, y = nn.Linear(4, 3), torch.randn(5, 4), torch.arange(5) % 3
        other = copy.deepcopy(model)
        a, b = torch.optim.SGD(model.parameters(), lr=.1), torch.optim.SGD(other.parameters(), lr=.1)
        F.cross_entropy(model(x), y).backward()
        a.step()
        self.assertFalse(c.amp_step(other, b, x, y)['amp_enabled'])
        for left, right in zip(model.parameters(), other.parameters()):
            torch.testing.assert_close(left, right)

    def test_cuda_amp_rejected_on_cpu_inputs(self):
        m = nn.Linear(4, 3)
        with self.assertRaises(RuntimeError):
            c.amp_step(m, torch.optim.SGD(m.parameters(), lr=.1), torch.ones(2, 4), torch.zeros(2, dtype=torch.long), True)

    def test_invalid_configuration(self):
        for cfg in (c.Config(batch_size=0), c.Config(classes=1), c.Config(dropout=1), c.Config(learning_rate=float('nan'))):
            with self.assertRaises(ValueError):
                cfg.validate()


class ArtifactTests(unittest.TestCase):
    def test_checkpoint_roundtrip_and_prediction(self):
        result = c.experiment(c.Config(epochs=2))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'model.pt'
            c.save_checkpoint(path, result['checkpoint'])
            loaded = c.load_checkpoint(path)
            for key, value in result['checkpoint']['model'].items():
                torch.testing.assert_close(loaded['model'][key], value)
            self.assertEqual(c.predict(loaded, [[1., 0., -.5, .2]]), c.predict(result['checkpoint'], [[1., 0., -.5, .2]]))
            with self.assertRaises(FileExistsError):
                c.save_checkpoint(path, loaded)

    def test_bad_checkpoint_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'bad.pt'
            torch.save({'format_version': -1}, path)
            with self.assertRaises(ValueError):
                c.load_checkpoint(path)

    def test_invalid_predict_input(self):
        payload = c.experiment(c.Config(epochs=1))['checkpoint']
        for rows in ([[1., 2.]], [[float('nan'), 1, 2, 3]]):
            with self.assertRaises(ValueError):
                c.predict(payload, rows)

    def test_resume_exact_cpu_epoch_boundary(self):
        cfg = c.Config(epochs=4)
        whole = c.experiment(cfg)
        half = c.experiment(cfg, stop_after=2)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'resume.pt'
            c.save_checkpoint(path, half['checkpoint'])
            resumed = c.experiment(cfg, resume=c.load_checkpoint(path))
        self.assertEqual(whole['history'], resumed['history'])
        for left, right in zip(whole['model'].parameters(), resumed['model'].parameters()):
            torch.testing.assert_close(left, right, atol=0, rtol=0)

    def test_resume_rejects_config_change(self):
        payload = c.experiment(c.Config(epochs=4), stop_after=1)['checkpoint']
        with self.assertRaises(ValueError):
            c.experiment(c.Config(epochs=5), resume=payload)
        payload['torch_version'] = 'different-build'
        with self.assertRaisesRegex(ValueError, 'same PyTorch'):
            c.experiment(c.Config(epochs=4), resume=payload)

    def test_actual_export_roundtrip(self):
        c.setup()
        with tempfile.TemporaryDirectory() as tmp:
            self.assertLess(c.export_roundtrip(c.TinyMLP(), torch.ones(2, 4), Path(tmp) / 'model.pt2'), 1e-6)

    def test_actual_compile_graph_capture(self):
        c.setup()
        model = c.TinyMLP(dropout=0).eval()
        x = torch.randn(2, 4)
        compiled = torch.compile(model, backend='eager', fullgraph=True)
        torch.testing.assert_close(model(x), compiled(x))

    def test_actual_cpu_profiler(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = entry(21).main([])
        self.assertTrue(result['has_teaching_step'])
        self.assertGreater(result['event_count'], 0)

    def test_all_24_default_entries_are_offline_from_other_cwd(self):
        before = Path.cwd()
        def denied(*args, **kwargs):
            raise AssertionError('Default examples must not open network connections')
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                with patch.object(socket.socket, 'connect', denied), patch.object(socket, 'create_connection', denied):
                    for number in range(1, 25):
                        with self.subTest(example=number), contextlib.redirect_stdout(io.StringIO()) as output:
                            result = entry(number).main([])
                            self.assertIsInstance(result, dict)
                            self.assertIsInstance(json.loads(output.getvalue()), dict)
            finally:
                os.chdir(before)


if __name__ == '__main__':
    unittest.main()
