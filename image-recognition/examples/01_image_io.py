"""Offline executable teaching example; run from this directory."""
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
from vision_core import load_rgb, chw_float, print_json

def main():
    with TemporaryDirectory() as folder:
        path=Path(folder)/'transparent.png'
        Image.new('RGBA',(8,6),(255,0,0,128)).save(path)
        image=load_rgb(path)
        tensor=chw_float(image)
        print_json({'size':image.size,'RGB':image.getpixel((0,0)),
                    'shape':list(tensor.shape),'dtype':str(tensor.dtype),
                    'range':[float(tensor.min()),float(tensor.max())]})

if __name__=='__main__': main()
