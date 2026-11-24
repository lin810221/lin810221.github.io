"""Original offline teaching experiment; keep lm_core.py with this file."""
import os
os.environ['HF_HUB_OFFLINE']='1'
os.environ['TOKENIZERS_PARALLELISM']='false'
from tempfile import TemporaryDirectory
import torch
from transformers import LlamaConfig,LlamaForCausalLM,TokenizersBackend
from lm_core import seed_everything,print_json
import importlib.util
from pathlib import Path

def tiny_hf():
    config=LlamaConfig(vocab_size=300,hidden_size=32,intermediate_size=64,num_hidden_layers=2,
        num_attention_heads=4,num_key_value_heads=2,max_position_embeddings=64,
        pad_token_id=0,bos_token_id=1,eos_token_id=2)
    config._attn_implementation='eager'
    return LlamaForCausalLM(config).eval()

def main():
    seed_everything();model=tiny_hf();ids=torch.tensor([[1,30,31,2]])
    spec=importlib.util.spec_from_file_location('local_bpe',Path(__file__).with_name('03_local_tokenizer.py'))
    local=importlib.util.module_from_spec(spec);spec.loader.exec_module(local)
    tokenizer=TokenizersBackend(tokenizer_object=local.build_tokenizer(),pad_token='<pad>',bos_token='<bos>',eos_token='<eos>')
    tokenizer.chat_template="{% for message in messages %}{{ '<bos>' + message['role'] + ': ' + message['content'] + '<eos>' }}{% endfor %}{% if add_generation_prompt %}{{ '<bos>assistant: ' }}{% endif %}"
    rendered=tokenizer.apply_chat_template([{'role':'user','content':'hello'}],tokenize=False,add_generation_prompt=True)
    with torch.inference_mode():reference=model(ids,use_cache=False).logits
    with TemporaryDirectory() as folder:
        model.save_pretrained(folder);tokenizer.save_pretrained(folder)
        restored=LlamaForCausalLM.from_pretrained(folder,local_files_only=True,attn_implementation='eager')
        with torch.inference_mode():error=float((restored(ids,use_cache=False).logits-reference).abs().max())
        reloaded=TokenizersBackend.from_pretrained(folder,local_files_only=True)
        assert reloaded.encode('hello')==tokenizer.encode('hello')
    print_json({'shape':list(reference.shape),'round_trip_max_error':error,'chat_template':rendered,
        'trained':False,'scope':'random tiny architecture and serialization; not a chat assistant'})

if __name__=='__main__':main()
