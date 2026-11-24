"""Offline executable teaching example; run from this directory."""
import torch
from torch import nn
from vision_core import seed_everything,print_json

def main():
    seed_everything()
    x=torch.randn(2,3,32,32)
    projection=nn.Conv2d(3,16,kernel_size=8,stride=8)
    tokens=projection(x).flatten(2).transpose(1,2)
    attention=nn.MultiheadAttention(16,4,batch_first=True,dropout=0.)
    output,weights=attention(tokens,tokens,tokens,need_weights=True)
    print_json({'patches':list(tokens.shape),'output':list(output.shape),
                'attention_row_sum':float(weights[0,0].sum().detach()),'trained':False})

if __name__=='__main__': main()
