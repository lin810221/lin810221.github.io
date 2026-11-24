"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from lm_core import print_json

def main():
    segments=torch.tensor([0,0,0,1,1])
    causal=torch.ones(5,5,dtype=torch.bool).tril()
    independent=causal&(segments[:,None]==segments[None,:])
    print_json({'document_segments':segments.tolist(),'stream_causal':causal.int().tolist(),
        'independent_documents':independent.int().tolist(),
        'note':'EOS alone does not block cross-document attention; choose training policy explicitly'})

if __name__=='__main__':main()
