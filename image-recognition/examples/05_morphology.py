"""Offline executable teaching example; run from this directory."""
import cv2
import numpy as np
from vision_core import print_json

def main():
    mask=np.zeros((16,16),dtype=np.uint8);mask[4:11,5:12]=1;mask[1,1]=1
    cleaned=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    n,labels,stats,centers=cv2.connectedComponentsWithStats(cleaned,connectivity=8)
    print_json({'foreground_components':n-1,'areas':stats[1:,cv2.CC_STAT_AREA].tolist(),
                'centroids':centers[1:].tolist(),'removed_pixels':int(mask.sum()-cleaned.sum())})

if __name__=='__main__': main()
