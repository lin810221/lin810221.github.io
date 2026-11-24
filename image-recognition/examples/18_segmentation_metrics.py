"""Offline executable teaching example; run from this directory."""
from vision_core import binary_mask_metrics,print_json

def main():
    target=[[1,1,0],[1,255,0]];prediction=[[1,0,0],[1,1,1]]
    report=binary_mask_metrics(prediction,target)
    print_json({'foreground':report,'absent_class':binary_mask_metrics([[0]],[[0]]),
                'all_ignored':binary_mask_metrics([[0]],[[255]])})

if __name__=='__main__': main()
