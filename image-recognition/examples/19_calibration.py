"""Offline executable teaching example; run from this directory."""
from vision_core import calibration,print_json

def main():
    y=[0,1,0,1,1,0,1,0]
    p=[.1,.8,.4,.7,.9,.2,.6,.3]
    print_json(calibration(p,y,bins=5))

if __name__=='__main__': main()
