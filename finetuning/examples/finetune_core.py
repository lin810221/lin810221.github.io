"""Offline, synthetic teaching experiments; no model download or service call.

The locally initialized model demonstrates training contracts, not the ability
of a pretrained LLM. All artifact operations use the caller's output directory.
"""
from __future__ import annotations
import copy, hashlib, json, math, os, random
from pathlib import Path
os.environ.setdefault('HF_HUB_OFFLINE','1')
os.environ.setdefault('TOKENIZERS_PARALLELISM','false')
os.environ.setdefault('WANDB_DISABLED','true')
import torch
import torch.nn.functional as F
from transformers import LlamaConfig, LlamaForCausalLM, PreTrainedTokenizerFast
from tokenizers import Tokenizer, models, pre_tokenizers

torch.set_num_threads(1)
SEED=41
VOCAB=['<pad>','<unk>','<bos>','<eos>','<system>','<user>','<assistant>',
       'classify','red','blue','green','warm','cool','unknown','answer','safe','unsafe']
TEMPLATE="""{% for message in messages %}{{ '<' + message['role'] + '> ' }}{% if message['role'] == 'assistant' %}{% generation %}{{ message['content'] + ' <eos> ' }}{% endgeneration %}{% else %}{{ message['content'] + ' <eos> ' }}{% endif %}{% endfor %}{% if add_generation_prompt %}{{ '<assistant> ' }}{% endif %}"""

def seed(n=SEED):
    random.seed(n);torch.manual_seed(n)

def tokenizer():
    backend=Tokenizer(models.WordLevel({v:i for i,v in enumerate(VOCAB)},unk_token='<unk>'))
    backend.pre_tokenizer=pre_tokenizers.WhitespaceSplit()
    tok=PreTrainedTokenizerFast(tokenizer_object=backend,unk_token='<unk>',pad_token='<pad>',
        bos_token='<bos>',eos_token='<eos>',additional_special_tokens=VOCAB[4:7])
    tok.chat_template=TEMPLATE
    return tok

def tiny_model():
    seed()
    return LlamaForCausalLM(LlamaConfig(vocab_size=len(VOCAB),hidden_size=32,
        intermediate_size=64,num_hidden_layers=1,num_attention_heads=4,
        num_key_value_heads=2,max_position_embeddings=128,attention_dropout=0.,
        pad_token_id=0,bos_token_id=2,eos_token_id=3,tie_word_embeddings=False,
        use_cache=False,_attn_implementation='eager'))

def records():
    rows=[]
    for group in range(12):
        color=['red','blue','green'][group%3];answer={'red':'warm','blue':'cool','green':'unknown'}[color]
        rows.append({'id':f'row-{group}','group':f'case-{group}', 'source':'course-synthetic-v1',
            'messages':[{'role':'user','content':f'classify {color}'},
                        {'role':'assistant','content':answer}]})
    return rows

def validate_rows(rows):
    ids=set()
    for row in rows:
        if not all(isinstance(row.get(k),str) and row[k].strip() for k in ['id','group','source']):
            raise ValueError('id, group and source are required')
        if row['id'] in ids:raise ValueError('duplicate id')
        ids.add(row['id']);messages=row.get('messages')
        if not isinstance(messages,list) or not messages:raise ValueError('empty messages')
        for i,m in enumerate(messages):
            if set(m)!={'role','content'} or m['role'] not in {'system','user','assistant'}:
                raise ValueError('unsupported message schema')
            if not isinstance(m['content'],str) or not m['content'].strip():raise ValueError('empty content')
            if m['role']=='system' and i!=0:raise ValueError('system must be first')
            if i and m['role']==messages[i-1]['role']:raise ValueError('repeated role')
        if messages[-1]['role']!='assistant':raise ValueError('missing assistant target')
    return len(ids)

def split_groups(rows,heldout_groups):
    validate_rows(rows)
    train=[r for r in rows if r['group'] not in heldout_groups]
    valid=[r for r in rows if r['group'] in heldout_groups]
    if not train or not valid:raise ValueError('empty split')
    assert not ({r['group'] for r in train}&{r['group'] for r in valid})
    return train,valid

def content_hash(row):
    return hashlib.sha256(json.dumps(row['messages'],ensure_ascii=False,sort_keys=True).encode()).hexdigest()

def duplicates(rows):
    groups={}
    for r in rows:groups.setdefault(content_hash(r),[]).append(r['id'])
    return [ids for ids in groups.values() if len(ids)>1]

def encode(row,tok=None,max_length=128):
    tok=tok or tokenizer()
    data=tok.apply_chat_template(row['messages'],tokenize=True,return_dict=True,
         return_assistant_tokens_mask=True,add_generation_prompt=False)
    ids=data['input_ids'];mask=data['assistant_masks']
    if len(ids)>max_length:raise ValueError('sequence too long: audit before truncation')
    labels=[v if m else -100 for v,m in zip(ids,mask)]
    if not any(v!=-100 for v in labels[1:]):raise ValueError('no supervised shifted targets')
    return {'input_ids':ids,'labels':labels,'attention_mask':[1]*len(ids)}

def collate(rows):
    length=max(len(r['input_ids']) for r in rows)
    return {k:torch.tensor([r[k]+[(-100 if k=='labels' else 0)]*(length-len(r[k])) for r in rows])
            for k in ['input_ids','labels','attention_mask']}

def shifted_loss(logits,labels,reduction='mean'):
    target=labels[:,1:];count=(target!=-100).sum()
    if not count:raise ValueError('no valid targets')
    total=F.cross_entropy(logits[:,:-1].reshape(-1,logits.shape[-1]),target.reshape(-1),
                          ignore_index=-100,reduction='sum')
    return total if reduction=='sum' else total/count

def batch():return collate([encode(r) for r in records()[:3]])

@torch.no_grad()
def evaluate(model,b):
    was=model.training;model.eval()
    logits=model(input_ids=b['input_ids'],attention_mask=b['attention_mask']).logits
    loss=shifted_loss(logits,b['labels']).item()
    valid=b['labels'][:,1:]!=-100
    correct=(logits[:,:-1].argmax(-1)==b['labels'][:,1:])[valid].sum().item()
    model.train(was)
    return {'nll':loss,'ppl':math.exp(loss),'teacher_forced_accuracy':correct/valid.sum().item(),
            'valid_targets':valid.sum().item()}

def train(model,b,steps=12,lr=.01):
    model.train();opt=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=lr)
    losses=[]
    for _ in range(steps):
        opt.zero_grad(set_to_none=True)
        loss=model(**b).loss;loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
        opt.step();losses.append(loss.item())
    return losses

def lora(model=None,rank=4,rs=False):
    from peft import LoraConfig,get_peft_model
    return get_peft_model(model or tiny_model(),LoraConfig(task_type='CAUSAL_LM',r=rank,
        lora_alpha=8,lora_dropout=0.,target_modules=['q_proj','v_proj'],bias='none',use_rslora=rs))

def count_parameters(model):
    return {'all':sum(p.numel() for p in model.parameters()),
            'trainable':sum(p.numel() for p in model.parameters() if p.requires_grad)}

def lora_matrix_demo():
    seed();a=torch.randn(2,3,requires_grad=True);b=torch.zeros(4,2,requires_grad=True)
    x=torch.randn(5,3);w=torch.randn(4,3);output=x@(w+4*b@a).T
    output.square().mean().backward()
    return {'delta_norm':(b@a).norm().item(),'A_grad':a.grad.norm().item(),'B_grad':b.grad.norm().item(),
            'adapter_parameters':a.numel()+b.numel()}

def accumulation_error():
    seed();a=torch.nn.Linear(3,2,bias=False);b=copy.deepcopy(a)
    xs=[torch.randn(1,3),torch.randn(4,3)];ys=[torch.tensor([0]),torch.tensor([1,0,1,1])]
    F.cross_entropy(a(torch.cat(xs)),torch.cat(ys)).backward()
    total=sum(len(y) for y in ys)
    for x,y in zip(xs,ys): (F.cross_entropy(b(x),y,reduction='sum')/total).backward()
    return (a.weight.grad-b.weight.grad).abs().max().item()

def memory_bytes(base_parameters,trainable_parameters,base_bits=4,activation_bytes=0):
    if min(base_parameters,trainable_parameters,activation_bytes)<0 or base_bits not in [4,8,16,32]:
        raise ValueError('invalid memory input')
    # Explicit model: base storage + FP32 adapters/grad/m/v. No master copy.
    return {'base':math.ceil(base_parameters*base_bits/8),
            'trainable_weights_grad_adam':trainable_parameters*4*4,
            'activations':activation_bytes}

def quantize_toy(values,bits=4):
    """Uniform symmetric quantizer, intentionally NOT the NF4 algorithm."""
    if bits<2 or bits>8:raise ValueError('bits must be 2..8')
    x=torch.tensor(values,dtype=torch.float32);qmax=2**(bits-1)-1
    scale=max(x.abs().max().item()/qmax,1e-12)
    q=(x/scale).round().clamp(-qmax,qmax).to(torch.int8)
    y=q.float()*scale
    return {'codes':q.tolist(),'scale':scale,'reconstructed':y.tolist(),'mse':(x-y).square().mean().item()}

def qlora_recipe():
    # This file never silently downloads weights or starts CUDA training.
    return {'requires':'CUDA-capable runtime and bitsandbytes==0.50.2; model-specific validation',
            'config':{'load_in_4bit':True,'bnb_4bit_quant_type':'nf4',
                      'bnb_4bit_use_double_quant':True,'bnb_4bit_compute_dtype':'bfloat16'},
            'order':['load quantized base','prepare_model_for_kbit_training','get_peft_model','audit trainable parameters'],
            'executed_gpu_training':False}

def sequence_logps(model,b):
    logits=model(input_ids=b['input_ids'],attention_mask=b['attention_mask']).logits[:,:-1]
    target=b['labels'][:,1:];mask=target!=-100
    if not torch.all(mask.sum(-1)>0):raise ValueError('empty completion')
    selected=F.log_softmax(logits.float(),-1).gather(-1,target.clamp_min(0).unsqueeze(-1)).squeeze(-1)
    return (selected*mask).sum(-1)

def dpo_loss(policy_chosen,policy_rejected,ref_chosen,ref_rejected,beta=.1):
    if beta<=0:raise ValueError('beta must be positive')
    margin=(policy_chosen-policy_rejected)-(ref_chosen.detach()-ref_rejected.detach())
    return -F.logsigmoid(beta*margin).mean()

def distillation(student_logits,teacher_logits,temperature=2.):
    if temperature<=0 or student_logits.shape!=teacher_logits.shape:raise ValueError('temperature or vocab mismatch')
    t=temperature
    return F.kl_div(F.log_softmax(student_logits/t,-1),F.softmax(teacher_logits.detach()/t,-1),
                    reduction='batchmean')*t*t

def state_hash(state):
    h=hashlib.sha256()
    for k,v in sorted(state.items()):
        h.update(k.encode());h.update(str(v.dtype).encode());h.update(str(tuple(v.shape)).encode())
        h.update(v.detach().cpu().contiguous().view(torch.uint8).numpy().tobytes())
    return h.hexdigest()

def tokenizer_hash(tok):
    return hashlib.sha256((tok.backend_tokenizer.to_str()+tok.chat_template).encode()).hexdigest()

def load_verified_adapter(base,folder,tok):
    from peft import PeftModel
    folder=Path(folder)
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    if state_hash(base.state_dict())!=manifest['base_sha256']:raise ValueError('base identity mismatch')
    if tokenizer_hash(tok)!=manifest['tokenizer_sha256']:raise ValueError('tokenizer or chat template mismatch')
    return PeftModel.from_pretrained(base,folder/'adapter')

def artifact_demo(folder):
    from peft import PeftModel
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    base=tiny_model();original=copy.deepcopy(base.state_dict());base_hash=state_hash(original)
    tok=tokenizer();model=lora(base);b=batch();train(model,b,steps=4)
    model.eval();before=model(**b).logits.detach()
    adapter=folder/'adapter';model.save_pretrained(adapter,safe_serialization=True);tok.save_pretrained(folder/'tokenizer')
    manifest={'schema':1,'base_sha256':base_hash,'tokenizer_sha256':tokenizer_hash(tok),
              'seed':SEED,'base':'locally initialized tiny Llama; not a pretrained checkpoint'}
    (folder/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    restored=tiny_model();restored.load_state_dict(original)
    loaded=load_verified_adapter(restored,folder,tok);loaded.eval()
    reloaded=loaded(**b).logits.detach();merged=loaded.merge_and_unload();merged.eval()
    after=merged(**b).logits.detach()
    return {'reload_max_abs':(before-reloaded).abs().max().item(),
            'merge_max_abs':(before-after).abs().max().item(),'manifest':manifest}

def resume_demo(folder):
    """Exact CPU comparison at optimizer boundary, deterministic one-batch order."""
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);seed()
    b=batch();model=tiny_model();opt=torch.optim.AdamW(model.parameters(),lr=.003)
    scheduler=torch.optim.lr_scheduler.LambdaLR(opt,lambda step:1-step/20)
    def step(m,o,s):
        m.train();o.zero_grad(set_to_none=True);loss=m(**b).loss;loss.backward();o.step();s.step()
    step(model,opt,scheduler)
    checkpoint={'model':model.state_dict(),'optimizer':opt.state_dict(),'scheduler':scheduler.state_dict(),
                'torch_rng':torch.get_rng_state(),'python_rng':random.getstate(),'optimizer_step':1,'data_offset':0}
    path=folder/'resume.pt';torch.save(checkpoint,path)
    step(model,opt,scheduler);target=copy.deepcopy(model.state_dict())
    # Only load a trusted checkpoint produced locally by this very experiment.
    state=torch.load(path,weights_only=False,map_location='cpu')
    restored=tiny_model();restored.load_state_dict(state['model'])
    ropt=torch.optim.AdamW(restored.parameters(),lr=.003)
    rs=torch.optim.lr_scheduler.LambdaLR(ropt,lambda step:1-step/20)
    # Scheduler construction initializes LR; restore optimizer AFTER construction.
    ropt.load_state_dict(state['optimizer']);rs.load_state_dict(state['scheduler'])
    torch.set_rng_state(state['torch_rng']);random.setstate(state['python_rng'])
    step(restored,ropt,rs)
    return max((target[k]-restored.state_dict()[k]).abs().max().item() for k in target)

def trl_sft(folder):
    from datasets import Dataset
    from trl import SFTConfig,SFTTrainer
    tok=tokenizer();dataset=Dataset.from_list([{'messages':r['messages']} for r in records()[:3]])
    args=SFTConfig(output_dir=str(folder),max_steps=2,per_device_train_batch_size=3,
        learning_rate=.003,report_to='none',save_strategy='no',logging_strategy='no',
        use_cpu=True,bf16=False,fp16=False,activation_checkpointing=False,
        dataloader_pin_memory=False,max_length=64,assistant_only_loss=True,seed=SEED)
    trainer=SFTTrainer(model=tiny_model(),args=args,train_dataset=dataset,processing_class=tok)
    result=trainer.train()
    return {'steps':trainer.state.global_step,'training_loss':result.training_loss}

def trl_dpo(folder):
    from datasets import Dataset
    from trl import DPOConfig,DPOTrainer
    seed();base=tiny_model();ref=copy.deepcopy(base);ref.requires_grad_(False);ref.eval();model=lora(base)
    ref_hash=state_hash(ref.state_dict())
    dataset=Dataset.from_list([{'prompt':'<user> classify red <eos> <assistant> ',
          'chosen':'warm <eos>','rejected':'cool <eos>'} for _ in range(3)])
    args=DPOConfig(output_dir=str(folder),max_steps=1,per_device_train_batch_size=3,
        learning_rate=.001,report_to='none',save_strategy='no',logging_strategy='no',
        use_cpu=True,bf16=False,fp16=False,activation_checkpointing=False,
        dataloader_pin_memory=False,max_length=64,beta=.1,seed=SEED)
    trainer=DPOTrainer(model=model,ref_model=ref,args=args,train_dataset=dataset,processing_class=tokenizer())
    result=trainer.train()
    return {'steps':trainer.state.global_step,'training_loss':result.training_loss,
            'reference_requires_grad':any(p.requires_grad for p in trainer.ref_model.parameters()),
            'reference_unchanged':ref_hash==state_hash(trainer.ref_model.state_dict())}

def heldout_demo():
    train_rows,valid_rows=split_groups(records(),{'case-9','case-10','case-11'})
    train_batch=collate([encode(r) for r in train_rows]);valid_batch=collate([encode(r) for r in valid_rows])
    model=tiny_model();before=evaluate(model,valid_batch);losses=train(model,train_batch)
    return {'before':before,'after':evaluate(model,valid_batch),'losses':losses,
            'limitation':'disjoint synthetic case IDs, but repeated templates/content; not semantic generalization'}

def job_trace(events):
    allowed={'created':{'validating'},'validating':{'running','failed'},'running':{'succeeded','failed','cancelled'},
             'succeeded':set(),'failed':set(),'cancelled':set()}
    state='created'
    for event in events:
        if event not in allowed[state]:raise ValueError(f'invalid job transition {state} -> {event}')
        state=event
    return state

def run(number,output=None):
    """24 deliberately small entrypoints with machine-readable outputs."""
    seed()
    if output is None:
        return run(number,Path.cwd()/'finetuning-output'/f'example-{number:02d}')
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    if number==1:return {'valid_rows':validate_rows(records()),'synthetic':True}
    if number==2:
        a,b=split_groups(records(),{'case-9','case-10','case-11'})
        return {'train':len(a),'valid':len(b),'duplicate_clusters':duplicates(records()),'warning':'group split alone does not remove cross-group duplicate content'}
    if number==3:
        r=encode(records()[0]);return {'tokens':tokenizer().convert_ids_to_tokens(r['input_ids']),**r}
    if number==4:
        b=batch();m=tiny_model();logits=m(**b).logits
        return {'manual':shifted_loss(logits,b['labels']).item(),'hf':m(**b).loss.item()}
    if number==5:
        r=encode(records()[0]);return {'length':len(r['input_ids']),'supervised':sum(x!=-100 for x in r['labels']),
            'packing':'EOS concatenation does not create cross-document attention isolation'}
    if number==6:
        m=tiny_model();b=batch();before=evaluate(m,b);losses=train(m,b)
        return {'before':before,'after':evaluate(m,b),'losses':losses}
    if number==7:return lora_matrix_demo()
    if number==8:
        m=lora();b=batch();before=evaluate(m,b);losses=train(m,b,steps=8)
        return {'parameters':count_parameters(m),'before':before,'after':evaluate(m,b),'losses':losses}
    if number==9:return {f'rank_{r}':{'counts':count_parameters(lora(rank=r)),
        'lora_scale':8/r,'rslora_scale':8/math.sqrt(r)} for r in [2,4,8]}
    if number==10:return {'method':'uniform symmetric toy, not NF4',**quantize_toy([-.9,-.3,0,.2,.7,1.])}
    if number==11:return qlora_recipe()
    if number==12:return {'max_gradient_error':accumulation_error()}
    if number==13:return memory_bytes(7_000_000_000,8_000_000,activation_bytes=2**30)
    if number==14:return {'resume_max_abs':resume_demo(out)}
    if number==15:return trl_sft(out)
    if number==16:
        m=tiny_model();b=batch();return {'completion_log_probability_sums':sequence_logps(m,b).detach().tolist()}
    if number==17:
        p=torch.tensor([2.],requires_grad=True);r=torch.tensor([1.],requires_grad=True)
        loss=dpo_loss(p,torch.zeros(1),r,torch.zeros(1),.2);loss.backward()
        return {'loss':loss.item(),'policy_gradient':p.grad.item(),'reference_gradient':None if r.grad is None else r.grad.item()}
    if number==18:return trl_dpo(out)
    if number==19:
        s=torch.tensor([[1.,0.,-1.]],requires_grad=True);t=torch.tensor([[2.,0.,-2.]],requires_grad=True)
        loss=distillation(s,t);loss.backward()
        return {'kd_loss':loss.item(),'teacher_gradient':None if t.grad is None else t.grad.tolist()}
    if number==20:return heldout_demo()
    if number==21:
        model=tiny_model();red=collate([encode(records()[0])]);blue=collate([encode(records()[1])])
        before=evaluate(model,blue);train(model,red,steps=20)
        return {'retention_before':before,'retention_after':evaluate(model,blue),'scope':'synthetic slice, not a universal forgetting result'}
    if number==22:return artifact_demo(out)
    if number==23:return {'final_state':job_trace(['validating','running','succeeded']),
        'network_calls':0,'note':'provider-neutral simulator; no cloud training or SDK request'}
    if number==24:
        report={'evaluation':heldout_demo(),'artifacts':artifact_demo(out/'artifact'),
            'resume':resume_demo(out/'checkpoint'),'synthetic':True,'seed':SEED}
        (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');return report
    raise ValueError('example number must be 1..24')

def cli(number):
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path)
    args=parser.parse_args();print(json.dumps(run(number,args.output),ensure_ascii=False,indent=2))
