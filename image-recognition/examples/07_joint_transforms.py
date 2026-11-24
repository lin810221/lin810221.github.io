"""Offline executable teaching example; run from this directory."""
import torch
from torchvision import tv_tensors
from torchvision.transforms import v2
from vision_core import make_shapes,seed_everything,print_json

def main():
    seed_everything()
    images,_,masks,boxes=make_shapes(2)
    transform=v2.Compose([v2.RandomHorizontalFlip(p=1.),v2.Resize((48,48)),
        v2.ToDtype({tv_tensors.Image:torch.float32,tv_tensors.Mask:torch.int64,
                    tv_tensors.BoundingBoxes:torch.float32,'others':None},scale=True)])
    image,box,mask=transform(tv_tensors.Image(images[0]),
        tv_tensors.BoundingBoxes(boxes[0:1],format='XYXY',canvas_size=(24,24)),
        tv_tensors.Mask(masks[0]))
    print_json({'image_shape':list(image.shape),'boxes':box.tolist(),
                'mask_dtype':str(mask.dtype),'mask_ids':torch.unique(mask).tolist()})

if __name__=='__main__': main()
