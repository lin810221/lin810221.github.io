"""Offline executable teaching example; run from this directory."""
import torch
from vision_core import train_classifier,make_shapes,print_json

def main():
    model,_=train_classifier()
    result={}
    with torch.inference_mode():
        for name,shift in [('same_generator',False),('inverted_brightness',True)]:
            x,y,_,_=make_shapes(48,seed=41,shift=shift)
            prediction=model(x).argmax(1)
            result[name]={'n':len(y),'accuracy':float((prediction==y).float().mean()),
                'class_recall':[float((prediction[y==c]==c).float().mean()) for c in [0,1]]}
    print_json(result)

if __name__=='__main__': main()
