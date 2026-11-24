"""Offline executable teaching example; run from this directory."""
import torch
from torch import nn
from torchvision.models import resnet18,ResNet18_Weights
from vision_core import seed_everything,print_json

def main():
    seed_everything()
    # No download: this proves shape/freezing only, NOT useful recognition.
    model=resnet18(weights=None)
    for parameter in model.parameters():parameter.requires_grad_(False)
    model.fc=nn.Linear(model.fc.in_features,2)
    model.eval() # freeze running BatchNorm state as well for this demonstration
    with torch.inference_mode():output=model(torch.zeros(2,3,64,64))
    preprocessing=ResNet18_Weights.IMAGENET1K_V1.transforms()
    print_json({'output':list(output.shape),'trainable_parameters':sum(p.numel() for p in model.parameters() if p.requires_grad),
                'trained':False,'pretrained_recipe':str(preprocessing)})

if __name__=='__main__': main()
