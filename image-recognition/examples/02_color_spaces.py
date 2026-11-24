"""Offline executable teaching example; run from this directory."""
import cv2
import numpy as np
from vision_core import print_json

def main():
    rgb=np.array([[[255,0,0],[0,255,0],[0,0,255]]],dtype=np.uint8)
    bgr=cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR)
    gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
    hsv=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV)
    print_json({'RGB':rgb.tolist(),'BGR':bgr.tolist(),'gray':gray.tolist(),
                'HSV_uint8':hsv.tolist(), 'hue_note':'OpenCV uint8 H normally 0..179'})

if __name__=='__main__': main()
