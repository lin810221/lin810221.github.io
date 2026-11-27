"""Optional real-model route: local weights + licensed JSONL, no downloads.

Full/LoRA on CPU or CUDA; QLoRA requires a compatible CUDA + bitsandbytes stack.
This route is provided for migration, not claimed as a pretrained/GPU benchmark.
"""
from pathlib import Path
import argparse, hashlib, json
import torch
from datasets import Dataset
from transformers import AutoModelForCausalLM,AutoTokenizer,BitsAndBytesConfig,set_seed
from peft import LoraConfig,get_peft_model,prepare_model_for_kbit_training
from trl import SFTConfig,SFTTrainer
from finetune_core import validate_rows,content_hash

def read_rows(path):
    rows=[json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
    if not rows:raise ValueError('empty dataset')
    validate_rows(rows);return rows

def file_hash(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def validate_splits(train_rows,valid_rows):
    if {r['id'] for r in train_rows}&{r['id'] for r in valid_rows}:raise ValueError('overlapping IDs')
    if {r['group'] for r in train_rows}&{r['group'] for r in valid_rows}:raise ValueError('overlapping groups')
    if {content_hash(r) for r in train_rows}&{content_hash(r) for r in valid_rows}:raise ValueError('exact content leakage')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model',type=Path,required=True,help='Existing local HF model directory')
    p.add_argument('--train',type=Path,required=True);p.add_argument('--valid',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--method',choices=['full','lora','qlora'],default='lora')
    p.add_argument('--targets',nargs='+',default=['q_proj','v_proj'])
    p.add_argument('--rank',type=int,default=8);p.add_argument('--alpha',type=int,default=16)
    p.add_argument('--max-length',type=int,default=512);p.add_argument('--steps',type=int,default=20)
    p.add_argument('--learning-rate',type=float,default=2e-5)
    p.add_argument('--seed',type=int,default=41)
    p.add_argument('--cpu',action='store_true');args=p.parse_args()
    if not args.model.is_dir():p.error('--model must already exist; this script never downloads weights')
    if min(args.rank,args.alpha,args.max_length,args.steps)<=0 or args.learning_rate<=0:p.error('positive settings required')
    if args.output.exists() and any(args.output.iterdir()):p.error('choose a new empty output directory')
    if args.output.resolve().is_relative_to(args.model.resolve()):p.error('output must be outside the base model directory')
    if args.method=='qlora' and (args.cpu or not torch.cuda.is_available()):p.error('QLoRA requires compatible CUDA hardware')
    train_rows=read_rows(args.train);valid_rows=read_rows(args.valid);validate_splits(train_rows,valid_rows)
    set_seed(args.seed)  # Seed BEFORE adapter initialization, not only inside Trainer.
    tok=AutoTokenizer.from_pretrained(args.model,local_files_only=True,trust_remote_code=False)
    if not tok.chat_template:raise ValueError('model needs an audited chat template')
    if tok.pad_token_id is None:tok.pad_token=tok.eos_token
    if tok.pad_token_id is None:raise ValueError('explicit padding policy required')
    for row in train_rows+valid_rows:
        encoded=tok.apply_chat_template(row['messages'],return_dict=True,tokenize=True,
            return_assistant_tokens_mask=True,add_generation_prompt=False)
        if len(encoded['input_ids'])>args.max_length:raise ValueError(f'audit truncation first: {row["id"]}')
        if not any(encoded.get('assistant_masks',[])[1:]):raise ValueError(f'no assistant supervision: {row["id"]}')
    use_cpu=args.cpu or not torch.cuda.is_available()
    bf16=not use_cpu and torch.cuda.is_bf16_supported()
    compute_dtype=torch.bfloat16 if bf16 else torch.float16
    # With FP16 autocast, retain ordinary trainable weights in FP32 for GradScaler.
    dtype=torch.bfloat16 if bf16 else torch.float32
    kwargs={'local_files_only':True,'trust_remote_code':False,'dtype':dtype}
    if args.method=='qlora':
        kwargs['quantization_config']=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=compute_dtype)
        kwargs['device_map']={'':torch.cuda.current_device()}  # Explicit single-process, single-GPU route.
    model=AutoModelForCausalLM.from_pretrained(args.model,**kwargs)
    model.config.use_cache=False
    if args.method=='qlora':model=prepare_model_for_kbit_training(model,use_gradient_checkpointing=False)
    if args.method!='full':
        model=get_peft_model(model,LoraConfig(task_type='CAUSAL_LM',r=args.rank,
            lora_alpha=args.alpha,lora_dropout=0.,target_modules=args.targets,bias='none'))
    trainable=sum(p.numel() for p in model.parameters() if p.requires_grad)
    if not trainable:raise ValueError('no trainable parameters')
    config=SFTConfig(output_dir=str(args.output),max_steps=args.steps,learning_rate=args.learning_rate,
        per_device_train_batch_size=1,per_device_eval_batch_size=1,gradient_accumulation_steps=1,
        max_length=args.max_length,assistant_only_loss=True,packing=False,
        activation_checkpointing=False,use_cpu=use_cpu,bf16=bf16,fp16=not use_cpu and not bf16,
        report_to='none',save_strategy='no',seed=args.seed,dataloader_pin_memory=not use_cpu)
    dataset=lambda rows:Dataset.from_list([{'messages':r['messages']} for r in rows])
    trainer=SFTTrainer(model=model,args=config,train_dataset=dataset(train_rows),
        eval_dataset=dataset(valid_rows),processing_class=tok)
    before=trainer.evaluate();trainer.train();after=trainer.evaluate()
    trainer.save_model(str(args.output/'model'));tok.save_pretrained(args.output/'tokenizer')
    manifest={'method':args.method,'base_directory':str(args.model.resolve()),
        'base_files':{f.relative_to(args.model).as_posix():file_hash(f) for f in sorted(args.model.rglob('*'))
            if f.is_file() and f.suffix in ['.json','.safetensors','.model','.bin','.txt','.jinja']},
        'data_sha256':{'train':file_hash(args.train),'valid':file_hash(args.valid)},
        'trainable_parameters':trainable,'before':before,'after':after,
        'settings':{k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},
        'limitation':'local single-process training; generation/task evaluation still required'}
    (args.output/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'output':str(args.output),'trainable':trainable,'before':before,'after':after},indent=2))

if __name__=='__main__':main()
