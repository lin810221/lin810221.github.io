"""Masked pooling and padding-row gradients."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    embedding=nn.Embedding(9,4,padding_idx=0)
    tokens=torch.tensor([[1,2,0,0],[3,4,5,0]])
    mask=tokens.ne(0);hidden=embedding(tokens)
    pooled=(hidden*mask.unsqueeze(-1)).sum(1)/mask.sum(1,keepdim=True)
    pooled.square().sum().backward()
    result={'pooled':pooled,'pad_gradient':embedding.weight.grad[0],
            'short_sequence_error':(pooled[0]-embedding(torch.tensor([1,2])).mean(0)).abs().max()}
    return emit(result)

if __name__=="__main__":
    main()
