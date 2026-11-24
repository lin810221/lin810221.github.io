"""Offline executable teaching example; run from this directory."""
import torch
from vision_core import print_json

def main():
    image=torch.arange(25,dtype=torch.float32).reshape(1,1,5,5)
    kernel=torch.tensor([[[[1.,0.,-1.],[1.,0.,-1.],[1.,0.,-1.]]]])
    valid=torch.nn.functional.conv2d(image,kernel)
    padded=torch.nn.functional.conv2d(image,kernel,padding=1,stride=2)
    print_json({'valid':valid.flatten().tolist(),'valid_shape':list(valid.shape),
                'stride2_padding1_shape':list(padded.shape),'kernel_sum':float(kernel.sum())})

if __name__=='__main__': main()
