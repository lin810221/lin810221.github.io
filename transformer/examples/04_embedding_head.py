"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from lm_core import TinyGPT,Config,seed_everything,print_json

def main():
    seed_everything();model=TinyGPT(Config(vocab_size=12,d_model=8,heads=2,layers=1,hidden=16))
    ids=torch.tensor([[1,4,4,2]])
    vectors=model.embedding(ids)
    logits=vectors@model.embedding.weight.T
    print_json({'ids':ids.tolist(),'embedding_shape':list(vectors.shape),
        'logit_shape':list(logits.shape),'tied_object':model.embedding.weight is model.head.weight,
        'repeated_id_same_vector':bool(torch.equal(vectors[0,1],vectors[0,2]))})

if __name__=='__main__':main()
