"""Offline executable teaching example; run from this directory."""
import torch
from torchvision import tv_tensors
from torchvision.transforms import v2
from vision_core import print_json

def main():
    mask=tv_tensors.Mask(torch.tensor([[0,1],[255,2]],dtype=torch.int64))
    resized=v2.Resize((8,8))(mask)
    logits=torch.zeros(1,3,8,8)
    loss=torch.nn.functional.cross_entropy(logits,resized.unsqueeze(0),ignore_index=255)
    print_json({'unique_ids':torch.unique(resized).tolist(),'dtype':str(resized.dtype),
                'CE_ignore255':float(loss),'valid_pixels':int((resized!=255).sum())})

if __name__=='__main__': main()
