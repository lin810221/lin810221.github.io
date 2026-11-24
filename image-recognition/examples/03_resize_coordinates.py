"""Offline executable teaching example; run from this directory."""
import torch
from vision_core import letterbox_geometry,map_boxes,print_json

def main():
    original=torch.tensor([[4.,2.,31.,17.]])
    geometry=letterbox_geometry(37,21,64)
    mapped=map_boxes(original,geometry)
    restored=map_boxes(mapped,geometry,inverse=True)
    print_json({'geometry':geometry,'mapped':mapped.tolist(),
                'restored':restored.tolist(),'max_error':float((original-restored).abs().max())})

if __name__=='__main__': main()
