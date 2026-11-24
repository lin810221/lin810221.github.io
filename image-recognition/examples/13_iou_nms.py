"""Offline executable teaching example; run from this directory."""
import torch
from torchvision.ops import batched_nms
from vision_core import box_iou,print_json

def main():
    boxes=torch.tensor([[0.,0.,10.,10.],[1.,1.,11.,11.],[1.,1.,11.,11.]])
    scores=torch.tensor([.9,.8,.7]);classes=torch.tensor([1,1,2])
    kept=batched_nms(boxes,scores,classes,.5)
    print_json({'IoU':box_iou(boxes,boxes).tolist(),'class_aware_kept':kept.tolist()})

if __name__=='__main__': main()
