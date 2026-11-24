"""Original offline teaching experiment; keep lm_core.py with this file."""
import os
os.environ['HF_HUB_OFFLINE']='1'
import importlib.util
from pathlib import Path
import torch
from transformers import DynamicCache
from lm_core import seed_everything,print_json

def main():
    spec=importlib.util.spec_from_file_location('hf_local',Path(__file__).with_name('24_hf_offline_model.py'))
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    seed_everything();model=helper.tiny_hf();ids=torch.tensor([[1,30,31,32,33]])
    with torch.inference_mode():
        full=model(ids,use_cache=False).logits
        cache=DynamicCache(config=model.config)
        model(ids[:,:3],cache=cache,use_cache=True)
        out=model(ids[:,3:],cache=cache,use_cache=True,attention_mask=torch.ones_like(ids),position_ids=torch.tensor([[3,4]]))
        error=float((full[:,3:]-out.logits).abs().max())
    print_json({'max_logit_error':error,'cache_length':out.cache.get_seq_length(),
        'key_shape':list(out.cache.layers[0].keys.shape),'preferred_API':'Transformers5.24 cache= / output.cache'})

if __name__=='__main__':main()
