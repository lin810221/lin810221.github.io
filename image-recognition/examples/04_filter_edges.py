"""Offline executable teaching example; run from this directory."""
import cv2
import numpy as np
from vision_core import print_json

def main():
    image=np.zeros((12,12),dtype=np.uint8);image[3:9,4:8]=255
    blurred=cv2.GaussianBlur(image,(3,3),0,borderType=cv2.BORDER_REFLECT_101)
    gradient=cv2.Sobel(image,cv2.CV_32F,1,0,ksize=3)
    edges=cv2.Canny(blurred,50,120)
    print_json({'edge_pixels':int((edges>0).sum()),
                'signed_gradient':[float(gradient.min()),float(gradient.max())],
                'blur_center':int(blurred[5,5])})

if __name__=='__main__': main()
