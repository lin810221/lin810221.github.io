"""Offline executable teaching example; run from this directory."""
import argparse
import torch
from vision_core import make_shapes,print_json,seed_everything

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--heavy',action='store_true')
    args=parser.parse_args();seed_everything()
    images,_,_,boxes=make_shapes(2)
    targets=[{'boxes':boxes[i:i+1],'labels':torch.ones(1,dtype=torch.int64)} for i in range(2)]
    result={'images':[list(x.shape) for x in images],
            'target_boxes':[t['boxes'].tolist() for t in targets],'trained':False}
    if args.heavy:
        from torchvision.models.detection import fasterrcnn_mobilenet_v3_large_320_fpn
        model=fasterrcnn_mobilenet_v3_large_320_fpn(weights=None,weights_backbone=None,
            num_classes=2,min_size=64,max_size=64,box_detections_per_img=5,
            rpn_pre_nms_top_n_test=20,rpn_post_nms_top_n_test=10).eval()
        with torch.inference_mode(): output=model(list(images))
        result['untrained_output_keys']=sorted(output[0])
    print_json(result)

if __name__=='__main__': main()
