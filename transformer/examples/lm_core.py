"""Inspectable, CPU-first decoder LM. Original toy data, no network/weights.

Manual model labels are shifted by the caller exactly once. Attention boolean
masks use True=allowed. Cache positions use physical past length; learned
position IDs use nonpadding token counts when a key mask is provided.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
import random

import torch
from torch import nn
from torch.nn import functional as F


def seed_everything(seed=24):
    random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


class ByteTokenizer:
    pad_id, bos_id, eos_id, vocab_size = 0, 1, 2, 259

    def encode(self, text, bos=True, eos=True):
        return ([self.bos_id] if bos else []) + [x+3 for x in text.encode('utf-8')] + ([self.eos_id] if eos else [])

    def decode(self, ids, errors='strict'):
        if any(type(x) is not int or x < 0 or x >= self.vocab_size for x in ids):
            raise ValueError('Unknown byte token ID')
        return bytes(x-3 for x in ids if x >= 3).decode('utf-8', errors=errors)


class TinyBPE:
    """Train-only byte BPE with deterministic ties and exact byte round trips.

    No normalization, regex pretokenizer, special IDs or vocabulary pruning.
    A decoded token may be an incomplete UTF-8 fragment; decode whole sequence.
    """
    def __init__(self):
        self.merges = []
        self.pieces = {i: bytes([i]) for i in range(256)}

    @staticmethod
    def merge(sequence, pair, new_id):
        result, i = [], 0
        while i < len(sequence):
            if i+1 < len(sequence) and (sequence[i], sequence[i+1]) == pair:
                result.append(new_id); i += 2
            else:
                result.append(sequence[i]); i += 1
        return result

    def fit(self, texts, steps=12):
        if self.merges or len(self.pieces) != 256:
            raise ValueError('Use a new tokenizer for a new training corpus')
        sequences = [list(x.encode('utf-8')) for x in texts]
        for _ in range(steps):
            counts = Counter(pair for s in sequences for pair in zip(s, s[1:]))
            if not counts:
                break
            pair = min(counts, key=lambda p: (-counts[p], p))
            new_id = len(self.pieces)
            self.pieces[new_id] = self.pieces[pair[0]] + self.pieces[pair[1]]
            self.merges.append((pair, new_id))
            sequences = [self.merge(s, pair, new_id) for s in sequences]
        return self

    def encode(self, text):
        result = list(text.encode('utf-8'))
        for pair, new_id in self.merges:
            result = self.merge(result, pair, new_id)
        return result

    def decode(self, ids):
        return b''.join(self.pieces[x] for x in ids).decode('utf-8')


def allowed_mask(query_length, key_length, past_length=0, device=None):
    if min(query_length, key_length) < 1 or past_length < 0 or key_length != past_length+query_length:
        raise ValueError('Append-only cache shape required')
    q = torch.arange(past_length, past_length+query_length, device=device)
    k = torch.arange(key_length, device=device)
    return k[None, :] <= q[:, None]


def reference_attention(q, k, v, allowed):
    if q.shape[-1] != k.shape[-1] or k.shape[-2] != v.shape[-2]:
        raise ValueError('Attention dimensions disagree')
    scores = q @ k.transpose(-1, -2) / math.sqrt(q.shape[-1])
    allowed = torch.broadcast_to(allowed.to(device=q.device, dtype=torch.bool), scores.shape)
    if not allowed.any(-1).all():
        raise ValueError('No allowed key for a query')
    weights = scores.masked_fill(~allowed, -torch.inf).softmax(-1)
    return weights @ v, weights


def rope(x, positions, base=10000.):
    if x.shape[-1] % 2 or base <= 0:
        raise ValueError('Even head dimension and positive base required')
    # Explicit adjacent-pair convention; other models may use split-half pairing.
    inv = base ** (-torch.arange(0, x.shape[-1], 2, device=x.device, dtype=x.dtype)/x.shape[-1])
    angle = positions.to(device=x.device, dtype=x.dtype)[..., None] * inv
    while angle.ndim < x.ndim:
        angle = angle.unsqueeze(0)
    a, b = x[..., 0::2], x[..., 1::2]
    return torch.stack((a*angle.cos()-b*angle.sin(), a*angle.sin()+b*angle.cos()), -1).flatten(-2)


@dataclass
class Config:
    vocab_size: int = 259
    d_model: int = 32
    heads: int = 4
    layers: int = 2
    context: int = 64
    hidden: int = 96
    dropout: float = 0.


class CausalAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        if config.d_model % config.heads:
            raise ValueError('d_model must divide heads')
        self.heads, self.head_dim = config.heads, config.d_model // config.heads
        self.qkv = nn.Linear(config.d_model, config.d_model*3, bias=False)
        self.output = nn.Linear(config.d_model, config.d_model, bias=False)
        self.dropout = config.dropout

    def forward(self, x, past=None, key_mask=None):
        b, t, d = x.shape
        q, k, v = (a.reshape(b,t,self.heads,self.head_dim).transpose(1,2) for a in self.qkv(x).chunk(3,-1))
        past_length = 0
        if past is not None:
            pk, pv = past
            if pk.shape != pv.shape or pk.shape[:2] != (b,self.heads) or pk.shape[-1] != self.head_dim:
                raise ValueError('Cache batch, heads or head dimension mismatch')
            past_length = pk.shape[-2]
            k, v = torch.cat((pk,k),-2), torch.cat((pv,v),-2)
        allowed = allowed_mask(t,k.shape[-2],past_length,x.device)[None,None]
        if key_mask is not None:
            if key_mask.shape != (b,k.shape[-2]):
                raise ValueError('Mask must cover the entire cached and new key sequence')
            allowed = allowed & key_mask[:,None,None,:].bool()
        if not allowed.any(-1).all():
            raise ValueError('This teaching model requires an allowed key for every query')
        y = F.scaled_dot_product_attention(q,k,v,attn_mask=allowed,
            dropout_p=self.dropout if self.training else 0.,is_causal=False)
        y = y.transpose(1,2).contiguous().view(b,t,d)
        return self.output(y), (k,v)


class Block(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.norm1, self.norm2 = nn.LayerNorm(config.d_model), nn.LayerNorm(config.d_model)
        self.attention = CausalAttention(config)
        self.ffn = nn.Sequential(nn.Linear(config.d_model,config.hidden),nn.GELU(),nn.Linear(config.hidden,config.d_model))
        self.dropout = nn.Dropout(config.dropout)

    def forward(self,x,past=None,key_mask=None):
        y,cache = self.attention(self.norm1(x),past,key_mask)
        x = x+self.dropout(y)
        return x+self.dropout(self.ffn(self.norm2(x))), cache


class TinyGPT(nn.Module):
    def __init__(self, config=None):
        super().__init__()
        self.config = config or Config()
        c = self.config
        self.embedding, self.position = nn.Embedding(c.vocab_size,c.d_model), nn.Embedding(c.context,c.d_model)
        self.blocks = nn.ModuleList(Block(c) for _ in range(c.layers))
        self.norm, self.head = nn.LayerNorm(c.d_model), nn.Linear(c.d_model,c.vocab_size,bias=False)
        self.apply(self.initialize)
        self.head.weight = self.embedding.weight  # Explicitly tied in this model.

    @staticmethod
    def initialize(module):
        if isinstance(module,(nn.Linear,nn.Embedding)):
            nn.init.normal_(module.weight,mean=0.,std=.02)
            if getattr(module,'bias',None) is not None:nn.init.zeros_(module.bias)

    def forward(self, ids, cache=None, attention_mask=None, use_cache=False):
        if ids.ndim != 2 or ids.dtype != torch.long or ids.shape[1] < 1:
            raise ValueError('Nonempty int64 [B,T] token IDs required')
        if ((ids<0)|(ids>=self.config.vocab_size)).any():
            raise ValueError('Token outside vocabulary')
        if cache is not None and len(cache) != self.config.layers:
            raise ValueError('One key/value cache per layer required')
        past = 0 if cache is None else cache[0][0].shape[-2]
        if cache is not None and any(k.shape[-2]!=past or v.shape[-2]!=past for k,v in cache):
            raise ValueError('All layers must share the same physical cache length')
        if past+ids.shape[1] > self.config.context:
            raise ValueError('Context exhausted: learned positions cannot be silently reset')
        if attention_mask is None:
            positions = torch.arange(past,past+ids.shape[1],device=ids.device)[None,:]
        else:
            if attention_mask.shape != (ids.shape[0],past+ids.shape[1]):
                raise ValueError('Full prefix attention mask required')
            if not ((attention_mask==0)|(attention_mask==1)).all():
                raise ValueError('Key mask values must be 0 or 1')
            positions = (attention_mask.long().cumsum(-1)-1).clamp(min=0)[:,-ids.shape[1]:]
        x = self.embedding(ids)+self.position(positions)
        new_cache=[]
        for i,block in enumerate(self.blocks):
            x,kv=block(x,None if cache is None else cache[i],attention_mask)
            new_cache.append(kv)
        return {'logits':self.head(self.norm(x)), 'cache':new_cache if use_cache else None}


def language_loss(logits, labels):
    if logits.shape[:-1] != labels.shape or labels.dtype != torch.long:
        raise ValueError('Logits [B,T,V] and int64 labels [B,T] required')
    valid=labels != -100
    if not valid.any():raise ValueError('No valid target token')
    total=F.cross_entropy(logits.reshape(-1,logits.shape[-1]),labels.reshape(-1),ignore_index=-100,reduction='sum')
    return total/valid.sum(), int(valid.sum())


def make_batch(texts, tokenizer=None, context=64):
    tok=tokenizer or ByteTokenizer()
    sequences=[tok.encode(s) for s in texts]
    if not sequences or any(len(s)-1>context for s in sequences):
        raise ValueError('Empty corpus or sequence longer than context')
    width=max(len(s)-1 for s in sequences)
    x=torch.full((len(sequences),width),tok.pad_id,dtype=torch.long)
    y=torch.full_like(x,-100)
    mask=torch.zeros_like(x,dtype=torch.bool)
    for i,s in enumerate(sequences):
        n=len(s)-1;x[i,:n]=torch.tensor(s[:-1]);y[i,:n]=torch.tensor(s[1:]);mask[i,:n]=True
    return x,y,mask


def toy_corpus():
    # Entirely original grammar; split by complete sentence before tokenization.
    subjects=['red bird','blue bird','green bird','small bird','red fish','blue fish','green fish','small fish']
    verbs=['moves','rests','turns','waits']
    sentences=[f'{s} {v}.\n' for s in subjects for v in verbs]
    valid=[x for i,x in enumerate(sentences) if i%5==0]
    train=[x for i,x in enumerate(sentences) if i%5!=0]
    return train,valid


def train_tiny(steps=140):
    seed_everything()
    model=TinyGPT();train,valid=toy_corpus()
    x,y,mask=make_batch(train);vx,vy,vm=make_batch(valid)
    optimizer=torch.optim.AdamW(model.parameters(),lr=.008,weight_decay=.01)
    model.train();history=[]
    for step in range(steps):
        optimizer.zero_grad(set_to_none=True)
        loss,count=language_loss(model(x,attention_mask=mask)['logits'],y)
        loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
        optimizer.step();history.append(float(loss.detach()))
    model.eval()
    with torch.inference_mode():
        valid_loss,valid_count=language_loss(model(vx,attention_mask=vm)['logits'],vy)
    return model,{'steps':steps,'train_sentences':len(train),'valid_sentences':len(valid),
        'first_train_nll':history[0],'last_train_nll':history[-1],
        'valid_nll':float(valid_loss),'valid_perplexity':math.exp(float(valid_loss)),
        'train_target_tokens':count,'valid_target_tokens':valid_count,'history':history}


def filter_logits(logits, temperature=1., top_k=None, top_p=1.):
    if logits.ndim != 1 or not torch.isfinite(logits).all() or temperature <= 0 or not math.isfinite(temperature):
        raise ValueError('Finite 1D logits and positive temperature required')
    if not 0 < top_p <= 1:raise ValueError('top_p must be in (0,1]')
    result=logits/temperature
    if top_k is not None:
        if type(top_k) is not int or not 1 <= top_k <= len(result):raise ValueError('Invalid top_k')
        # Stable order makes ties explicit; exactly k kept.
        order=torch.argsort(result,descending=True,stable=True)
        keep=torch.zeros_like(result,dtype=torch.bool);keep[order[:top_k]]=True
        result=result.masked_fill(~keep,-torch.inf)
    order=torch.argsort(result,descending=True,stable=True)
    probs=result[order].softmax(-1)
    remove=probs.cumsum(-1)-probs >= top_p  # retain the token crossing p
    result=result.clone();result[order[remove]]=-torch.inf
    return result


@torch.inference_mode()
def generate(model, ids, max_new_tokens=12, use_cache=True, sample=False, seed=24, temperature=1.,top_k=None,top_p=1.):
    if model.training:raise ValueError('Call eval before generation')
    if ids.ndim != 2 or ids.shape[0]!=1:raise ValueError('Teaching generator supports one unpadded sequence')
    if type(max_new_tokens) is not int or max_new_tokens<0 or ids.shape[1]+max_new_tokens>model.config.context:
        raise ValueError('Requested generation exceeds context budget')
    result=ids.clone();cache=None;generator=torch.Generator(device=ids.device).manual_seed(seed)
    for _ in range(max_new_tokens):
        current=result if cache is None else result[:,-1:]
        out=model(current,cache=cache,use_cache=use_cache)
        logits=out['logits'][0,-1]
        if sample:
            probs=filter_logits(logits,temperature,top_k,top_p).softmax(-1)
            token=torch.multinomial(probs,1,generator=generator).item()
        else:token=int(logits.argmax())
        result=torch.cat((result,result.new_tensor([[token]])),1)
        cache=out['cache'] if use_cache else None
        if token==ByteTokenizer.eos_id:break
    return result


def kv_bytes(batch,layers,length,kv_heads,head_dim,bytes_per_element=2):
    values=[batch,layers,length,kv_heads,head_dim,bytes_per_element]
    if any(type(x) is not int or x<1 for x in values):raise ValueError('Positive integer capacities required')
    return 2*batch*layers*length*kv_heads*head_dim*bytes_per_element


def save_artifact(model,folder,report=None):
    from safetensors.torch import save_model
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    save_model(model,str(folder/'model.safetensors'))
    (folder/'config.json').write_text(json.dumps(asdict(model.config),indent=2),encoding='utf-8')
    (folder/'tokenizer.json').write_text(json.dumps({'type':'original-byte','pad':0,'bos':1,'eos':2,'byte_offset':3,'normalization':'none'}),encoding='utf-8')
    manifest={'schema':1,'model':'original-tiny-gpt','synthetic_grammar':True,
        'labels_shift':'external-once','cache_mask':'True means allowed','weights_tied':True,
        'sha256':hashlib.sha256((folder/'model.safetensors').read_bytes()).hexdigest()}
    (folder/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    if report is not None:
        (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
        history=report.get('history',[])
        if history:
            maximum=max(history);points=' '.join(f'{70+i*520/max(1,len(history)-1):.2f},{250-v/maximum*200:.2f}' for i,v in enumerate(history))
            ticks=''.join(f'<text x="58" y="{255-fraction*200}" text-anchor="end" fill="#c1d2c8" font-size="16">{maximum*fraction:.2f}</text>' for fraction in [0,.5,1])
            ticks+=''.join(f'<text x="{70+fraction*520}" y="276" text-anchor="middle" fill="#c1d2c8" font-size="16">{1+round(fraction*(len(history)-1))}</text>' for fraction in [0,.5,1])
            svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 330" role="img" aria-labelledby="title"><title id="title">Original toy language model training NLL</title><rect width="650" height="330" fill="#111b18"/><g font-family="Arial,sans-serif"><path d="M70 40V250H600" fill="none" stroke="#77958b"/>{ticks}<polyline points="{points}" fill="none" stroke="#a6ddce" stroke-width="3"/><text x="70" y="27" fill="#e6eee8" font-size="18">Train NLL per valid target token</text><text x="330" y="312" text-anchor="middle" fill="#e6eee8" font-size="18">Update step</text></g></svg>'
            (folder/'loss.svg').write_text(svg,encoding='utf-8')
    return manifest


def load_artifact(folder):
    from safetensors.torch import load_model
    folder=Path(folder)
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    if hashlib.sha256((folder/'model.safetensors').read_bytes()).hexdigest()!=manifest['sha256']:
        raise ValueError('Model hash does not match manifest')
    model=TinyGPT(Config(**json.loads((folder/'config.json').read_text(encoding='utf-8'))))
    load_model(model,str(folder/'model.safetensors'),strict=True)
    return model.eval()


def print_json(value):
    print(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False))
