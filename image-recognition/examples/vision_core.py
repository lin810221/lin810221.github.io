"""Small, deterministic vision experiments. Images are original synthetic data.

No network calls, pretrained weights or external datasets. XYXY coordinates
describe continuous half-open boundaries; all areas omit the legacy +1.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageOps, ImageDraw
from torch import nn
from torch.utils.data import Dataset


def seed_everything(seed=23):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def load_rgb(path):
    """Apply EXIF once, explicitly composite alpha over white, then RGB."""
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source)
        if image.mode in ('RGBA', 'LA') or 'transparency' in image.info:
            rgba = image.convert('RGBA')
            base = Image.new('RGBA', rgba.size, (255, 255, 255, 255))
            image = Image.alpha_composite(base, rgba)
        return image.convert('RGB').copy()


def chw_float(image):
    array = np.asarray(image, dtype=np.uint8).copy()
    if array.ndim != 3 or array.shape[2] != 3:
        raise ValueError('Expected RGB HWC uint8 image')
    return torch.from_numpy(array).permute(2, 0, 1).float() / 255


def validate_boxes(boxes, width=None, height=None):
    b = torch.as_tensor(boxes, dtype=torch.float32)
    if b.ndim != 2 or b.shape[1] != 4 or not torch.isfinite(b).all():
        raise ValueError('Expected finite [N,4] XYXY boxes')
    if ((b[:, 2:] - b[:, :2]) <= 0).any():
        raise ValueError('Boxes must have positive area')
    if width is not None and ((b[:, [0, 2]] < 0).any() or (b[:, [0, 2]] > width).any()):
        raise ValueError('Box outside image width')
    if height is not None and ((b[:, [1, 3]] < 0).any() or (b[:, [1, 3]] > height).any()):
        raise ValueError('Box outside image height')
    return b


def box_iou(a, b):
    a, b = validate_boxes(a), validate_boxes(b)
    lt = torch.maximum(a[:, None, :2], b[None, :, :2])
    rb = torch.minimum(a[:, None, 2:], b[None, :, 2:])
    intersection = (rb - lt).clamp(min=0).prod(-1)
    aa = (a[:, 2:] - a[:, :2]).prod(-1)
    ab = (b[:, 2:] - b[:, :2]).prod(-1)
    return intersection / (aa[:, None] + ab[None, :] - intersection)


def flip_boxes(boxes, width):
    b = validate_boxes(boxes, width=width).clone()
    left = width - b[:, 2].clone()
    b[:, 2] = width - b[:, 0]
    b[:, 0] = left
    return b


def letterbox_geometry(width, height, size=64):
    if any(type(v) is not int or v < 1 for v in (width, height, size)):
        raise ValueError('Positive integer dimensions required')
    scale = min(size / width, size / height)
    nw, nh = max(1, round(width * scale)), max(1, round(height * scale))
    # Actual axis scales include integer rounding; do not invert nominal scale.
    return {'size': (nw, nh), 'scale': (nw / width, nh / height),
            'offset': ((size - nw) // 2, (size - nh) // 2)}


def map_boxes(boxes, geometry, inverse=False):
    b = validate_boxes(boxes).clone()
    sx, sy = geometry['scale']
    dx, dy = geometry['offset']
    scale = b.new_tensor([sx, sy, sx, sy])
    offset = b.new_tensor([dx, dy, dx, dy])
    return (b - offset) / scale if inverse else b * scale + offset


def group_split(records, seed=23):
    groups = sorted({r['group'] for r in records})
    if len(groups) < 5:
        raise ValueError('Need at least five independent groups for this demo')
    random.Random(seed).shuffle(groups)
    a, b = max(1, int(.6 * len(groups))), max(2, int(.8 * len(groups)))
    membership = {g: split for split, gs in zip(('train', 'valid', 'test'),
                    (groups[:a], groups[a:b], groups[b:])) for g in gs}
    return {split: [r for r in records if membership[r['group']] == split]
            for split in ('train', 'valid', 'test')}


def make_shapes(n=96, size=24, seed=23, shift=False):
    """Square vs narrow vertical rectangle. Masks also provide exact boxes.

    Synthetic shape semantics do not transfer to natural image accuracy.
    """
    if n < 2 or size < 16:
        raise ValueError('Need n>=2 and image size>=16')
    rng = np.random.default_rng(seed)
    images, labels, masks, boxes = [], [], [], []
    for i in range(n):
        label = i % 2
        w, h = (10, 10) if label == 0 else (4, 14)
        x, y = int(rng.integers(1, size - w)), int(rng.integers(1, size - h))
        mask = np.zeros((size, size), dtype=np.int64)
        mask[y:y+h, x:x+w] = 1
        noise = rng.uniform(0, .08, (3, size, size)).astype('float32')
        image = noise + mask[None].astype('float32') * .8
        if shift:
            image = 1 - image  # deliberately new acquisition condition
        images.append(image); labels.append(label); masks.append(mask)
        boxes.append([x, y, x+w, y+h])
    return (torch.from_numpy(np.stack(images)), torch.tensor(labels),
            torch.from_numpy(np.stack(masks)), torch.tensor(boxes, dtype=torch.float32))


class ShapeDataset(Dataset):
    def __init__(self, n=96, seed=23):
        self.images, self.labels, self.masks, self.boxes = make_shapes(n, seed=seed)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        return self.images[index], self.labels[index]


class TinyClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(nn.Conv2d(3, 8, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2), nn.Conv2d(8, 12, 3, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d((3, 3)))
        self.head = nn.Linear(108, 2)

    def forward(self, x):
        return self.head(self.features(x).flatten(1))


def train_classifier(steps=100):
    seed_everything()
    model = TinyClassifier()
    x, y, _, _ = make_shapes(96)
    vx, vy, _, _ = make_shapes(48, seed=41)
    optimizer = torch.optim.AdamW(model.parameters(), lr=.012, weight_decay=.001)
    history = []
    model.train()
    for _ in range(steps):
        optimizer.zero_grad(set_to_none=True)
        loss = nn.functional.cross_entropy(model(x), y)
        loss.backward(); optimizer.step(); history.append(float(loss.detach()))
    model.eval()
    with torch.inference_mode():
        accuracy = float((model(vx).argmax(1) == vy).float().mean())
    return model, {'first_loss': history[0], 'last_loss': history[-1],
                   'valid_accuracy': accuracy, 'steps': steps}


class TinySegmenter(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Conv2d(3, 8, 3, padding=1), nn.ReLU(), nn.Conv2d(8, 2, 1))

    def forward(self, x):
        return self.net(x)


def train_segmenter(steps=35):
    seed_everything()
    model = TinySegmenter()
    x, _, y, _ = make_shapes(32)
    optimizer = torch.optim.AdamW(model.parameters(), lr=.025)
    losses = []
    for _ in range(steps):
        optimizer.zero_grad(set_to_none=True)
        loss = nn.functional.cross_entropy(model(x), y)
        loss.backward(); optimizer.step(); losses.append(float(loss.detach()))
    model.eval()
    vx, _, vy, _ = make_shapes(16, seed=41)
    with torch.inference_mode():
        metrics = binary_mask_metrics(model(vx).argmax(1).numpy(), vy.numpy())
    return model, dict(first_loss=losses[0], last_loss=losses[-1], **metrics)


def binary_mask_metrics(pred, target, ignore=255):
    pred, target = np.asarray(pred), np.asarray(target)
    if pred.shape != target.shape or pred.size == 0:
        raise ValueError('Nonempty masks of equal shape required')
    valid = target != ignore
    if not valid.any():
        return {'iou': None, 'dice': None, 'valid_pixels': 0}
    if not np.isin(pred[valid], [0, 1]).all() or not np.isin(target[valid], [0, 1]).all():
        raise ValueError('Binary class IDs required; threshold probabilities first')
    p, t = (pred == 1) & valid, (target == 1) & valid
    intersection, union = int((p & t).sum()), int((p | t).sum())
    denominator = int(p.sum() + t.sum())
    # Undefined absent class is explicit; callers must state averaging policy.
    return {'iou': intersection / union if union else None,
            'dice': 2 * intersection / denominator if denominator else None,
            'valid_pixels': int(valid.sum())}


def toy_ap(predictions, truths, threshold=.5):
    """Single class, per-image one-to-one matching; all-points envelope AP.

    Not COCO evaluation: no crowd/ignore/area/maxDets/101-point sampling.
    predictions=[{image,box,score}], truths={image:[box,...]}.
    """
    if not 0 <= threshold <= 1:
        raise ValueError('IoU threshold must be in [0,1]')
    count = sum(len(v) for v in truths.values())
    if not count:
        raise ValueError('AP undefined without ground-truth positives')
    used = {image: set() for image in truths}
    for boxes in truths.values():
        validate_boxes(torch.tensor(boxes).reshape(-1, 4))
    rows, tp, fp = [], 0, 0
    for item in sorted(predictions, key=lambda p: -p['score']):
        if not math.isfinite(item['score']) or not 0 <= item['score'] <= 1:
            raise ValueError('Finite probability score required')
        validate_boxes([item['box']])
        image = item['image']; boxes = truths.get(image, [])
        available = [j for j in range(len(boxes)) if j not in used.get(image, set())]
        if available:
            values = box_iou([item['box']], [boxes[j] for j in available])[0]
            best = int(values.argmax()); matched = float(values[best]) >= threshold
        else:
            matched = False
        if matched:
            tp += 1; used[image].add(available[best])
        else:
            fp += 1
        rows.append({'tp': matched, 'precision': tp / (tp+fp), 'recall': tp / count})
    envelope = [r['precision'] for r in rows]
    for i in range(len(envelope)-2, -1, -1):
        envelope[i] = max(envelope[i], envelope[i+1])
    ap, previous = 0., 0.
    for r, precision in zip(rows, envelope):
        ap += (r['recall'] - previous) * precision; previous = r['recall']
    return {'ap': ap, 'rows': rows, 'positives': count, 'policy': 'toy-all-points'}


def confusion_matrix(target, prediction, classes=2):
    y, p = np.asarray(target), np.asarray(prediction)
    if y.shape != p.shape or y.ndim != 1 or y.size == 0:
        raise ValueError('Equal nonempty label vectors required')
    if not np.issubdtype(y.dtype, np.integer) or not np.issubdtype(p.dtype, np.integer):
        raise ValueError('Integer class IDs required')
    if ((y < 0) | (y >= classes) | (p < 0) | (p >= classes)).any():
        raise ValueError('Label outside classes')
    return np.bincount(classes*y+p, minlength=classes**2).reshape(classes, classes)


def calibration(probabilities, target, bins=5):
    p, y = np.asarray(probabilities, dtype=float), np.asarray(target)
    if p.shape != y.shape or p.ndim != 1 or not p.size or bins < 1:
        raise ValueError('Equal nonempty binary vectors required')
    if not np.isfinite(p).all() or ((p < 0) | (p > 1)).any() or not np.isin(y, [0, 1]).all():
        raise ValueError('Binary targets and valid probabilities required')
    index = np.minimum((p * bins).astype(int), bins-1)
    rows, ece = [], 0.
    for b in range(bins):
        selected = index == b
        if not selected.any():
            continue
        mean_p, frequency = float(p[selected].mean()), float(y[selected].mean())
        n = int(selected.sum()); ece += n / len(p) * abs(mean_p-frequency)
        rows.append({'n': n, 'probability': mean_p, 'frequency': frequency})
    # This is class-1 probability calibration, not top-label confidence ECE.
    return {'ece': ece, 'brier': float(np.mean((p-y)**2)), 'bins': rows}


def artifact_contract(model_path, labels=('square', 'bar')):
    path = Path(model_path)
    return {'schema': 1, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'labels': list(labels), 'input': {'layout': 'NCHW', 'channels': 3,
            'height': 24, 'width': 24, 'dtype': 'float32', 'range': [0, 1],
            'color': 'RGB', 'exif': 'transpose-once', 'alpha': 'white'},
            'output': {'kind': 'logits', 'classes': 2}, 'synthetic_demo': True}


def print_json(value):
    print(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False))


def save_preview(folder, images, report, *, prediction=None, target=None, boxes=None, true_boxes=None):
    """Save original generated images plus optional masks or boxes for inspection.

    The input images remain 0..1 RGB. Predicted boxes are cyan, truths amber.
    Each row includes image, target mask and predicted mask when available.
    """
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True)
    count = min(8, len(images)); size = 120
    columns = 3 if prediction is not None and target is not None else 1
    sheet = Image.new('RGB', (size*columns, size*count), '#111c17')
    for i in range(count):
        array = (images[i].detach().cpu().permute(1,2,0).numpy().clip(0,1)*255).round().astype('uint8')
        tile = Image.fromarray(array).resize((size,size), Image.Resampling.NEAREST)
        draw = ImageDraw.Draw(tile)
        for collection, color in [(true_boxes, '#ebc782'), (boxes, '#a6ddce')]:
            if collection is not None:
                # Display inclusive endpoints are derived from half-open edges.
                x1,y1,x2,y2 = (collection[i].detach().cpu().numpy() * size / images.shape[-1]).tolist()
                draw.rectangle((x1,y1,max(x1,x2-1),max(y1,y2-1)),outline=color,width=2)
        sheet.paste(tile,(0,i*size))
        if columns==3:
            for col,masks in [(1,target),(2,prediction)]:
                mask=(masks[i].detach().cpu().numpy()==1).astype('uint8')*255
                sheet.paste(Image.fromarray(mask).convert('RGB').resize((size,size),Image.Resampling.NEAREST),(col*size,i*size))
    sheet.save(folder/'preview.png')
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    return folder/'preview.png'
