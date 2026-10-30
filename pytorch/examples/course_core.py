"""Real PyTorch teaching tools; course target torch 2.15.0 / Python 3.11.

All data are synthetic. Default examples use CPU, no downloads or remote APIs.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import random
import torch
from torch import nn
from torch.nn import functional as F
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset


@dataclass(frozen=True)
class Config:
    seed: int = 7
    features: int = 4
    hidden: int = 12
    classes: int = 3
    batch_size: int = 16
    epochs: int = 10
    learning_rate: float = 0.03
    dropout: float = 0.1

    def validate(self):
        for value in (self.features, self.hidden, self.classes, self.batch_size, self.epochs):
            if not isinstance(value, int) or value < 1:
                raise ValueError("Positive integer dimensions and budgets required")
        if self.classes < 2 or not 0 <= self.dropout < 1 or not math.isfinite(self.learning_rate) or self.learning_rate <= 0:
            raise ValueError("Invalid class count, dropout, or learning rate")


def setup(seed=7):
    """One thread keeps tiny teaching workloads fast; not a universal tuning rule."""
    torch.set_num_threads(1)
    torch.manual_seed(seed)
    random.seed(seed)


def choose_device(name="cpu"):
    if name == "auto":
        name = "cuda" if torch.cuda.is_available() else "cpu"
    if name not in {"cpu", "cuda"}:
        raise ValueError("Teaching examples support cpu, cuda or auto")
    if name == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is unavailable; choose CPU or install a compatible build")
    return torch.device(name)


class FeatureDataset(Dataset):
    def __init__(self, x, y):
        if x.ndim != 2 or y.ndim != 1 or len(x) != len(y) or len(x) == 0:
            raise ValueError("Expected nonempty X[N,F], y[N]")
        if not x.is_floating_point() or y.dtype != torch.long:
            raise ValueError("Floating features and long class indices required")
        if not torch.isfinite(x).all():
            raise ValueError("Nonfinite features")
        self.x, self.y = x, y

    def __len__(self):
        return len(self.y)

    def __getitem__(self, index):
        return self.x[index], self.y[index]


def make_data(config=Config()):
    """Disjoint synthetic train/validation/test; preprocessing fits train only."""
    config.validate()
    generator = torch.Generator().manual_seed(config.seed + 100)
    x = torch.randn(160, config.features, generator=generator)
    teacher = torch.randn(config.features, config.classes, generator=generator)
    y = (x @ teacher).argmax(dim=1)
    order = torch.randperm(len(y), generator=generator)
    x, y = x[order], y[order]
    train_x, train_y = x[:96], y[:96]
    mean = train_x.mean(dim=0)
    scale = train_x.std(dim=0, unbiased=False).clamp_min(1e-6)
    split = [FeatureDataset((values - mean) / scale, labels) for values, labels in
             ((train_x, train_y), (x[96:128], y[96:128]), (x[128:], y[128:]))]
    return split, {"mean": mean, "scale": scale}


def seed_worker(worker_id):
    # torch's worker seed is set by DataLoader; seed Python's random as well.
    del worker_id
    random.seed(torch.initial_seed() % (2 ** 32))


def make_loaders(config=Config(), workers=0):
    if workers < 0:
        raise ValueError("Nonnegative worker count required")
    splits, preprocessing = make_data(config)
    generator = torch.Generator().manual_seed(config.seed + 33)
    train = DataLoader(splits[0], batch_size=config.batch_size, shuffle=True, generator=generator,
                       num_workers=workers, worker_init_fn=seed_worker)
    validation = DataLoader(splits[1], batch_size=config.batch_size, shuffle=False, num_workers=0)
    test = DataLoader(splits[2], batch_size=config.batch_size, shuffle=False, num_workers=0)
    return (train, validation, test), preprocessing, generator


def collate_sequences(rows):
    if not rows or any(len(tokens) == 0 for tokens, _ in rows):
        raise ValueError("Nonempty sequences required")
    sequences = [torch.as_tensor(tokens, dtype=torch.long) for tokens, _ in rows]
    padded = pad_sequence(sequences, batch_first=True, padding_value=0)
    labels = torch.tensor([label for _, label in rows], dtype=torch.long)
    return padded, padded.ne(0), labels


class TinyMLP(nn.Module):
    def __init__(self, features=4, hidden=12, classes=3, dropout=0.1):
        super().__init__()
        self.network = nn.Sequential(nn.Linear(features, hidden), nn.ReLU(), nn.Dropout(dropout), nn.Linear(hidden, classes))

    def forward(self, x):
        return self.network(x)  # Raw logits, no softmax before CrossEntropyLoss.


class SequenceClassifier(nn.Module):
    def __init__(self, vocabulary=8, dimensions=4, classes=2):
        super().__init__()
        self.embedding = nn.Embedding(vocabulary, dimensions, padding_idx=0)
        self.head = nn.Linear(dimensions, classes)

    def forward(self, tokens, mask):
        if tokens.shape != mask.shape or torch.any(mask.sum(dim=1) == 0):
            raise ValueError("A matching mask with at least one token per sequence is required")
        hidden = self.embedding(tokens)
        pooled = (hidden * mask.unsqueeze(-1)).sum(dim=1) / mask.sum(dim=1, keepdim=True)
        return self.head(pooled)


def train_epoch(model, loader, optimizer, device="cpu"):
    model.train()
    loss_sum, correct, count = 0.0, 0, 0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad(set_to_none=True)
        logits = model(x)
        loss = F.cross_entropy(logits, y)
        loss.backward()
        optimizer.step()
        n = y.numel()
        loss_sum += loss.detach().item() * n
        correct += logits.detach().argmax(dim=1).eq(y).sum().item()
        count += n
    if count == 0:
        raise ValueError("Empty loader")
    return {"loss": loss_sum / count, "accuracy": correct / count, "samples": count}


@torch.inference_mode()
def evaluate(model, loader, device="cpu"):
    previous_mode = model.training
    model.eval()
    loss_sum, correct, count = 0.0, 0, 0
    try:
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            logits = model(x)
            loss_sum += F.cross_entropy(logits, y, reduction="sum").item()
            correct += logits.argmax(dim=1).eq(y).sum().item()
            count += y.numel()
        if not count:
            raise ValueError("Empty loader")
        return {"loss": loss_sum / count, "accuracy": correct / count, "samples": count}
    finally:
        model.train(previous_mode)


def frozen_state(model):
    return {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}


def experiment(config=Config(), device="cpu", stop_after=None, resume=None):
    """Epoch-boundary resume includes optimizer, CPU RNG, and loader generator.

    Exact equality is verified only for the CPU setup; no mid-epoch promise.
    """
    config.validate()
    setup(config.seed)
    device = choose_device(device)
    loaders, preprocessing, generator = make_loaders(config)
    train, validation, test = loaders
    model = TinyMLP(config.features, config.hidden, config.classes, config.dropout).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    initial = evaluate(model, validation, device)
    start, history = 0, []
    best_loss, best_state = math.inf, frozen_state(model)
    if resume is not None:
        if resume.get("format_version") != 1 or resume["config"] != asdict(config):
            raise ValueError("Checkpoint configuration mismatch")
        if resume.get("torch_version") != str(torch.__version__):
            raise ValueError("Exact resume requires the same PyTorch build")
        if device.type != "cpu":
            raise ValueError("This exact-resume teaching path is CPU-only")
        model.load_state_dict(resume["model"])
        optimizer.load_state_dict(resume["optimizer"])
        torch.set_rng_state(resume["torch_rng"])
        generator.set_state(resume["loader_rng"])
        start, history = resume["epoch"], list(resume["history"])
        best_loss, best_state = resume["best_loss"], resume["best_model"]
    stop = config.epochs if stop_after is None else min(stop_after, config.epochs)
    if stop < start:
        raise ValueError("Cannot resume backwards")
    for epoch in range(start, stop):
        training = train_epoch(model, train, optimizer, device)
        metrics = evaluate(model, validation, device)
        history.append({"epoch": epoch + 1, "train_loss": training["loss"], "validation_loss": metrics["loss"]})
        if metrics["loss"] < best_loss:
            best_loss, best_state = metrics["loss"], frozen_state(model)
    payload = {"format_version": 1, "config": asdict(config), "epoch": stop,
        "model": frozen_state(model), "optimizer": optimizer.state_dict(),
        "torch_rng": torch.get_rng_state(), "loader_rng": generator.get_state(),
        "best_model": best_state, "best_loss": best_loss, "history": history,
        "preprocessing": preprocessing, "torch_version": str(torch.__version__)}
    # Test data are evaluated only after the complete configured run.
    final = evaluate(model, validation, device)
    test_metrics = None
    if stop == config.epochs:
        best_model = TinyMLP(config.features, config.hidden, config.classes, config.dropout).to(device)
        best_model.load_state_dict(best_state)
        test_metrics = evaluate(best_model, test, device)
    return {"model": model, "checkpoint": payload, "initial_validation": initial,
            "final_validation": final, "test": test_metrics, "history": history}


def save_checkpoint(path, payload):
    path = Path(path)
    if path.exists():
        raise FileExistsError("Choose a new checkpoint filename; existing files are preserved")
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(payload, path)


def load_checkpoint(path):
    # Only load a checkpoint whose source you trust, even with weights_only.
    payload = torch.load(path, map_location="cpu", weights_only=True)
    if not isinstance(payload, dict) or payload.get("format_version") != 1:
        raise ValueError("Unknown checkpoint format")
    return payload


def predict(checkpoint, raw_features):
    config = Config(**checkpoint["config"])
    values = torch.as_tensor(raw_features, dtype=torch.float32)
    if values.ndim != 2 or values.shape[1] != config.features or not torch.isfinite(values).all():
        raise ValueError("Expected finite feature rows with the configured width")
    preprocessing = checkpoint["preprocessing"]
    normalized = (values - preprocessing["mean"]) / preprocessing["scale"]
    model = TinyMLP(config.features, config.hidden, config.classes, config.dropout)
    model.load_state_dict(checkpoint["best_model"])
    model.eval()
    with torch.inference_mode():
        return model(normalized).argmax(dim=1).tolist()


def accumulated_step(model, optimizer, microbatches):
    """Exact sample-weighted mean for one effective group, including its tail.

    Equivalence to a large batch assumes no batch-dependent/stochastic behavior.
    """
    total = sum(len(y) for _, y in microbatches)
    if total == 0:
        raise ValueError("Empty accumulation group")
    optimizer.zero_grad(set_to_none=True)
    for x, y in microbatches:
        loss = F.cross_entropy(model(x), y, reduction="sum") / total
        loss.backward()
    optimizer.step()


def amp_step(model, optimizer, x, y, use_cuda_amp=False):
    if use_cuda_amp and (x.device.type != "cuda" or not torch.cuda.is_available()):
        raise RuntimeError("CUDA AMP requires CUDA model and tensors")
    scaler = torch.amp.GradScaler("cuda", enabled=use_cuda_amp)
    optimizer.zero_grad(set_to_none=True)
    with torch.autocast(device_type="cuda" if use_cuda_amp else "cpu", dtype=torch.float16 if use_cuda_amp else torch.bfloat16, enabled=use_cuda_amp):
        loss = F.cross_entropy(model(x), y)
    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)
    gradient_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=100.0)
    scaler.step(optimizer)
    scaler.update()
    return {"loss": loss.detach().item(), "gradient_norm": gradient_norm.item(), "amp_enabled": use_cuda_amp}


def export_roundtrip(model, sample, path):
    model.eval()
    program = torch.export.export(model, (sample,))
    torch.export.save(program, str(path))
    loaded = torch.export.load(str(path))
    with torch.inference_mode():
        error = (model(sample) - loaded.module()(sample)).abs().max().item()
    return error


def custom_dataset():
    path = Path(__file__).parent / "data" / "custom_samples.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    return FeatureDataset(torch.tensor([row["features"] for row in rows], dtype=torch.float32),
                          torch.tensor([row["label"] for row in rows], dtype=torch.long))
