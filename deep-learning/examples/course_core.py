"""Original CPU deep-learning experiments, PyTorch 2.15.0. Synthetic data only."""
from __future__ import annotations
import json
import math
from pathlib import Path
import torch
from torch import nn
from torch.nn import functional as F
from torch.nn.utils.rnn import pad_sequence,pack_padded_sequence
from torch.utils.data import Dataset,DataLoader,TensorDataset

SEED=7

def setup(seed=SEED):
    torch.set_num_threads(1)
    torch.manual_seed(seed)

def emit(report):
    def convert(value):
        if isinstance(value,torch.Tensor):return value.detach().cpu().tolist()
        raise TypeError(type(value).__name__)
    plain=json.loads(json.dumps(report,default=convert,allow_nan=False))
    print(json.dumps(plain,indent=2,allow_nan=False))
    return plain

def snapshot(model):
    return {key:value.detach().cpu().clone() for key,value in model.state_dict().items()}

class MLP(nn.Module):
    def __init__(self,width=24):
        super().__init__()
        self.layers=nn.Sequential(nn.Linear(4,width),nn.ReLU(),nn.Linear(width,width),nn.ReLU(),nn.Linear(width,2))
    def forward(self,x):return self.layers(x)

class TinyCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers=nn.Sequential(nn.Conv2d(1,6,3,padding=1),nn.ReLU(),
            nn.Conv2d(6,8,3,stride=2,padding=1),nn.ReLU(),nn.Flatten(1),nn.Linear(128,2))
    def forward(self,x):return self.layers(x)

class TokenDataset(Dataset):
    def __init__(self,rows):self.rows=rows
    def __len__(self):return len(self.rows)
    def __getitem__(self,index):return self.rows[index]

def collate_tokens(rows):
    if not rows or any(not len(tokens) for tokens,_ in rows):raise ValueError('Nonempty token sequences required')
    tokens=[torch.as_tensor(row,dtype=torch.long) for row,_ in rows]
    if any(torch.any(t<=0) or torch.any(t>=9) for t in tokens):raise ValueError('Token IDs must be 1..8; zero is PAD')
    return pad_sequence(tokens,batch_first=True,padding_value=0),torch.tensor([len(t) for t in tokens]),torch.tensor([y for _,y in rows])

class SequenceModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding=nn.Embedding(9,8,padding_idx=0)
        self.gru=nn.GRU(8,12,batch_first=True)
        self.head=nn.Linear(12,2)
    def forward(self,tokens,lengths):
        if lengths.ndim!=1 or len(lengths)!=len(tokens) or torch.any(lengths<1) or torch.any(lengths>tokens.shape[1]):
            raise ValueError('Invalid sequence lengths')
        packed=pack_padded_sequence(self.embedding(tokens),lengths.cpu(),batch_first=True,enforce_sorted=False)
        _,hidden=self.gru(packed)
        return self.head(hidden[-1])

def make_data(kind='tabular',seed=SEED):
    g=torch.Generator().manual_seed(seed+100)
    preprocessing={}
    if kind=='tabular':
        x=torch.randn(480,4,generator=g)
        y=(x[:,0]*x[:,1]+.25*x[:,2]-.1*x[:,3]>0).long()
        order=torch.randperm(len(y),generator=g);x,y=x[order],y[order]
        mean=x[:288].mean(0);scale=x[:288].std(0,unbiased=False).clamp_min(1e-6)
        x=(x-mean)/scale;preprocessing={'mean':mean,'scale':scale}
        splits=[TensorDataset(x[a:b],y[a:b]) for a,b in [(0,288),(288,384),(384,480)]]
    elif kind=='image':
        x=.15*torch.randn(180,1,8,8,generator=g);y=torch.arange(180)%2
        for i in range(len(y)):
            start=int(torch.randint(1,6,(1,),generator=g))
            if y[i]:x[i,0,:,start:start+2]+=1
            else:x[i,0,start:start+2,:]+=1
        order=torch.randperm(len(y),generator=g);x,y=x[order],y[order]
        splits=[TensorDataset(x[a:b],y[a:b]) for a,b in [(0,108),(108,144),(144,180)]]
    elif kind=='sequence':
        rows=[]
        for _ in range(240):
            length=int(torch.randint(2,8,(1,),generator=g))
            tokens=torch.randint(1,9,(length,),generator=g).tolist()
            rows.append((tokens,int(tokens[-1]>=5)))
        order=torch.randperm(len(rows),generator=g).tolist();rows=[rows[i] for i in order]
        splits=[TokenDataset(rows[a:b]) for a,b in [(0,144),(144,192),(192,240)]]
    else:raise ValueError('Unknown teaching task')
    return splits,preprocessing

def build_model(kind):
    if kind=='tabular':return MLP()
    if kind=='image':return TinyCNN()
    if kind=='sequence':return SequenceModel()
    raise ValueError('Unknown model kind')

def make_loaders(kind='tabular',seed=SEED):
    splits,preprocessing=make_data(kind,seed)
    collate=collate_tokens if kind=='sequence' else None
    generator=torch.Generator().manual_seed(seed+33)
    loaders=[DataLoader(dataset,batch_size=24,shuffle=i==0,collate_fn=collate,
                        generator=generator if i==0 else None,num_workers=0) for i,dataset in enumerate(splits)]
    return loaders,preprocessing

def train_epoch(model,loader,optimizer):
    model.train();total=correct=count=0
    for *inputs,y in loader:
        optimizer.zero_grad(set_to_none=True)
        logits=model(*inputs);loss=F.cross_entropy(logits,y)
        loss.backward();optimizer.step()
        total+=loss.detach().item()*len(y);correct+=int((logits.detach().argmax(1)==y).sum());count+=len(y)
    if not count:raise ValueError('Empty loader')
    return {'loss':total/count,'accuracy':correct/count,'samples':count}

@torch.inference_mode()
def evaluate(model,loader):
    mode=model.training;model.eval();total=correct=count=0
    try:
        for *inputs,y in loader:
            logits=model(*inputs);total+=F.cross_entropy(logits,y,reduction='sum').item()
            correct+=int((logits.argmax(1)==y).sum());count+=len(y)
        if not count:raise ValueError('Empty loader')
        return {'loss':total/count,'accuracy':correct/count,'samples':count}
    finally:model.train(mode)

def experiment(kind='tabular',epochs=None,seed=SEED):
    epochs=epochs if epochs is not None else {'tabular':24,'image':10,'sequence':12}.get(kind,0)
    if not isinstance(epochs,int) or epochs<1:raise ValueError('Positive epoch budget required')
    setup(seed);loaders,preprocessing=make_loaders(kind,seed);train,validation,test=loaders
    model=build_model(kind);optimizer=torch.optim.AdamW(model.parameters(),lr=.02,weight_decay=.001)
    initial=evaluate(model,validation);history=[];best_loss=math.inf;best=snapshot(model)
    for epoch in range(epochs):
        training=train_epoch(model,train,optimizer);metrics=evaluate(model,validation)
        history.append({'epoch':epoch+1,'train_loss':training['loss'],'validation_loss':metrics['loss']})
        if metrics['loss']<best_loss:best_loss=metrics['loss'];best=snapshot(model)
    model.load_state_dict(best)
    payload={'format_version':1,'kind':kind,'seed':seed,'epochs':epochs,'state':best,
       'preprocessing':preprocessing,'torch_version':str(torch.__version__),'history':history,
       'schema':['x0','x1','x2','x3'] if kind=='tabular' else None}
    return {'model':model,'artifact':payload,'initial_validation':initial,
            'best_validation':evaluate(model,validation),'test':evaluate(model,test),'history':history}

def save_artifact(path,payload):
    path=Path(path)
    if path.exists():raise FileExistsError('Choose a new artifact filename')
    path.parent.mkdir(parents=True,exist_ok=True);torch.save(payload,path)

def load_artifact(path):
    # Only trusted checkpoints, even with weights_only=True.
    payload=torch.load(path,map_location='cpu',weights_only=True)
    if not isinstance(payload,dict) or payload.get('format_version')!=1:raise ValueError('Unknown artifact')
    if payload['torch_version']!=str(torch.__version__):raise ValueError('Use the verified PyTorch build')
    return payload

def predict_tabular(payload,rows):
    if payload['kind']!='tabular' or payload.get('schema')!=['x0','x1','x2','x3']:raise ValueError('Expected tabular artifact')
    x=torch.as_tensor(rows,dtype=torch.float32)
    if x.ndim!=2 or x.shape[1]!=4 or not len(x) or not torch.isfinite(x).all():raise ValueError('Expected finite X[N,4]')
    model=MLP();model.load_state_dict(payload['state']);model.eval()
    with torch.inference_mode():
        p=model((x-payload['preprocessing']['mean'])/payload['preprocessing']['scale']).softmax(1)
    return {'probabilities':p.tolist(),'labels':p.argmax(1).tolist()}

def prediction_rows():
    return json.loads((Path(__file__).parent/'data/prediction_rows.json').read_text(encoding='utf-8'))

def manual_chain(x=2.,w1=.3,b1=-.1,w2=-.7,b2=.2,target=.8):
    h=1/(1+math.exp(-(w1*x+b1)));prediction=w2*h+b2;error=prediction-target
    da=error*w2*h*(1-h)
    return {'hidden':h,'prediction':prediction,'loss':.5*error*error,
            'w1':da*x,'b1':da,'w2':error*h,'b2':error}

def softmax_gradient(logits,labels):
    return (logits.softmax(-1)-F.one_hot(labels,logits.shape[-1]))/len(labels)

def receptive_field(layers):
    field,jump=1,1
    for kernel,stride,dilation in layers:
        if min(kernel,stride,dilation)<1:raise ValueError('Positive convolution settings required')
        field+=(kernel-1)*dilation*jump;jump*=stride
    return {'field':field,'jump':jump}

def contrastive_loss(a,b,temperature=.2):
    if temperature<=0 or not math.isfinite(temperature) or a.shape!=b.shape or a.ndim!=2 or len(a)<2:
        raise ValueError('Matching batches and positive temperature required')
    if torch.any(a.norm(dim=1)==0) or torch.any(b.norm(dim=1)==0):raise ValueError('Nonzero vectors required')
    logits=F.normalize(a,dim=1)@F.normalize(b,dim=1).t()/temperature
    labels=torch.arange(len(a),device=a.device)
    return (F.cross_entropy(logits,labels)+F.cross_entropy(logits.t(),labels))/2

class TinyBlock(nn.Module):
    def __init__(self):
        super().__init__();self.norm1=nn.LayerNorm(8);self.norm2=nn.LayerNorm(8)
        self.attention=nn.MultiheadAttention(8,2,dropout=0,batch_first=True)
        self.ffn=nn.Sequential(nn.Linear(8,16),nn.GELU(),nn.Linear(16,8))
    def forward(self,x):
        mask=torch.ones(x.shape[1],x.shape[1],device=x.device,dtype=torch.bool).triu(1)
        z=self.norm1(x);x=x+self.attention(z,z,z,attn_mask=mask,need_weights=False)[0]
        return x+self.ffn(self.norm2(x))

class TinyVAE(nn.Module):
    def __init__(self):
        super().__init__();self.encoder=nn.Sequential(nn.Linear(2,12),nn.Tanh())
        self.mean=nn.Linear(12,2);self.logvar=nn.Linear(12,2)
        self.decoder=nn.Sequential(nn.Linear(2,12),nn.Tanh(),nn.Linear(12,2))
    def encode(self,x):
        h=self.encoder(x);return self.mean(h),self.logvar(h)
    def forward(self,x):
        mean,logvar=self.encode(x);z=mean+torch.exp(.5*logvar)*torch.randn_like(mean)
        return self.decoder(z),mean,logvar

def kl_standard_normal(mean,logvar):
    if mean.shape!=logvar.shape:raise ValueError('Matching latent shapes required')
    return .5*(mean.square()+logvar.exp()-1-logvar).sum(-1)

def generative_data(n=160):
    g=torch.Generator().manual_seed(107);u=torch.randn(n,1,generator=g)
    return torch.cat([u,.5*u.square()-.5],dim=1)

def train_autoencoder():
    setup();x=generative_data()
    model=nn.Sequential(nn.Linear(2,8),nn.Tanh(),nn.Linear(8,1),nn.Linear(1,8),nn.Tanh(),nn.Linear(8,2))
    optimizer=torch.optim.Adam(model.parameters(),lr=.03)
    initial=F.mse_loss(model(x),x).item()
    for _ in range(120):
        optimizer.zero_grad(set_to_none=True);loss=F.mse_loss(model(x),x);loss.backward();optimizer.step()
    return {'model':model,'initial_mse':initial,'final_mse':F.mse_loss(model(x),x).item()}

def train_vae():
    setup();x=generative_data();model=TinyVAE();optimizer=torch.optim.Adam(model.parameters(),lr=.02)
    with torch.no_grad():initial=F.mse_loss(model.decoder(model.encode(x)[0]),x).item()
    for _ in range(140):
        optimizer.zero_grad(set_to_none=True);reconstruction,mean,logvar=model(x)
        reconstruction_loss=.5*(reconstruction-x).square().sum(1).mean()
        kl=kl_standard_normal(mean,logvar).mean();loss=reconstruction_loss+.1*kl
        loss.backward();optimizer.step()
    with torch.no_grad():final=F.mse_loss(model.decoder(model.encode(x)[0]),x).item()
    return {'model':model,'initial_mean_decode_mse':initial,'final_mean_decode_mse':final,'last_kl':kl.item(),'beta':.1}

def gan_discriminator_step(generator,discriminator,optimizer,real,z):
    optimizer.zero_grad(set_to_none=True)
    fake=generator(z).detach()
    loss=F.binary_cross_entropy_with_logits(discriminator(real),torch.ones(len(real),1))
    loss+=F.binary_cross_entropy_with_logits(discriminator(fake),torch.zeros(len(fake),1))
    loss.backward();optimizer.step();return loss.detach().item()

def gan_generator_step(generator,discriminator,optimizer,z):
    optimizer.zero_grad(set_to_none=True)
    flags=[p.requires_grad for p in discriminator.parameters()]
    for p in discriminator.parameters():p.requires_grad_(False)
    try:
        loss=F.binary_cross_entropy_with_logits(discriminator(generator(z)),torch.ones(len(z),1))
        loss.backward();optimizer.step()
    finally:
        for p,flag in zip(discriminator.parameters(),flags):p.requires_grad_(flag)
    return loss.detach().item()

def train_gan():
    setup();generator=nn.Sequential(nn.Linear(2,12),nn.Tanh(),nn.Linear(12,2))
    discriminator=nn.Sequential(nn.Linear(2,12),nn.Tanh(),nn.Linear(12,1))
    opt_g=torch.optim.Adam(generator.parameters(),lr=.01);opt_d=torch.optim.Adam(discriminator.parameters(),lr=.01)
    for _ in range(120):
        real=.3*torch.randn(32,2)+torch.tensor([2.,-1.]);z=torch.randn(32,2)
        d=gan_discriminator_step(generator,discriminator,opt_d,real,z)
        g=gan_generator_step(generator,discriminator,opt_g,torch.randn(32,2))
    with torch.no_grad():sample_mean=generator(torch.randn(100,2)).mean(0)
    return {'last_discriminator_loss':d,'last_generator_loss':g,'sample_mean':sample_mean,
            'scope':'alternating-gradient mechanism only; GAN convergence is not guaranteed'}

def noise_schedule(steps=30):
    if not isinstance(steps,int) or steps<2:raise ValueError('At least two noise steps required')
    beta=torch.linspace(.03,.2,steps);alpha=1-beta;bar=alpha.cumprod(0)
    previous=torch.cat([torch.ones(1),bar[:-1]])
    return beta,alpha,bar,beta*(1-previous)/(1-bar)

def q_sample(clean,indices,epsilon,bar):
    if clean.shape!=epsilon.shape or indices.shape!=(len(clean),):raise ValueError('Noise shape mismatch')
    factor=bar[indices].reshape(-1,*([1]*(clean.ndim-1)))
    return factor.sqrt()*clean+(1-factor).sqrt()*epsilon

class TimeDenoiser(nn.Module):
    def __init__(self):
        super().__init__();self.network=nn.Sequential(nn.Linear(2,24),nn.SiLU(),nn.Linear(24,24),nn.SiLU(),nn.Linear(24,1))
    def forward(self,x,time):return self.network(torch.cat([x,time],1))

@torch.inference_mode()
def diffusion_sample(model,n=32,steps=30):
    beta,alpha,bar,variance=noise_schedule(steps);model.eval();x=torch.randn(n,1)
    for t in reversed(range(steps)):
        epsilon=model(x,torch.full((n,1),t/(steps-1)))
        mean=(x-beta[t]/(1-bar[t]).sqrt()*epsilon)/alpha[t].sqrt()
        x=mean+variance[t].sqrt()*torch.randn_like(x) if t>0 else mean
    return x

def train_diffusion():
    setup();beta,alpha,bar,variance=noise_schedule();model=TimeDenoiser();optimizer=torch.optim.Adam(model.parameters(),lr=.008)
    clean=2*(torch.arange(128)%2).float().unsqueeze(1)-1;clean=2*clean+.2*torch.randn_like(clean)
    probe_t=torch.randint(0,len(beta),(len(clean),));probe_epsilon=torch.randn_like(clean)
    probe_x=q_sample(clean,probe_t,probe_epsilon,bar);probe_time=probe_t.float().unsqueeze(1)/(len(beta)-1)
    initial=F.mse_loss(model(probe_x,probe_time),probe_epsilon).item()
    for _ in range(220):
        t=torch.randint(0,len(beta),(len(clean),));epsilon=torch.randn_like(clean)
        noisy=q_sample(clean,t,epsilon,bar);optimizer.zero_grad(set_to_none=True)
        loss=F.mse_loss(model(noisy,t.float().unsqueeze(1)/(len(beta)-1)),epsilon)
        loss.backward();optimizer.step()
    final=F.mse_loss(model(probe_x,probe_time),probe_epsilon).item();sample=diffusion_sample(model)
    return {'initial_probe_mse':initial,'final_probe_mse':final,'sample_mean':sample.mean().item(),
       'sample_std':sample.std().item(),'terminal_alpha_bar':bar[-1].item(),
       'scope':'one-dimensional toy DDPM; no image generation quality claim'}

def flow_path(noise,target,time):
    if noise.shape!=target.shape or time.shape!=(len(noise),1):raise ValueError('Flow path shape mismatch')
    return (1-time)*noise+time*target,target-noise

def train_flow():
    setup();model=TimeDenoiser();optimizer=torch.optim.Adam(model.parameters(),lr=.01)
    for _ in range(180):
        noise=torch.randn(128,1);target=2+.5*torch.randn(128,1);time=torch.rand(128,1)
        x,velocity=flow_path(noise,target,time);optimizer.zero_grad(set_to_none=True)
        loss=F.mse_loss(model(x,time),velocity);loss.backward();optimizer.step()
    with torch.inference_mode():
        x=torch.randn(64,1)
        for step in range(30):x=x+model(x,torch.full((len(x),1),step/30))/30
    return {'last_velocity_mse':loss.item(),'sample_mean':x.mean().item(),'sample_std':x.std().item(),
       'scope':'one-dimensional conditional flow matching with Euler sampling; no production quality claim'}

def distillation_loss(student_logits,teacher_logits,labels,temperature=2.,hard_weight=.5):
    if temperature<=0 or not math.isfinite(temperature) or not 0<=hard_weight<=1:raise ValueError('Invalid distillation settings')
    hard=F.cross_entropy(student_logits,labels)
    soft=F.kl_div(F.log_softmax(student_logits/temperature,1),F.softmax(teacher_logits.detach()/temperature,1),reduction='batchmean')*temperature**2
    return hard_weight*hard+(1-hard_weight)*soft
