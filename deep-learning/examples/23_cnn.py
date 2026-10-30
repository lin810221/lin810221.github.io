"""Train a tiny CNN on generated horizontal/vertical bands."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import experiment

def main(argv=None):
    del argv
    setup()
    run=experiment('image')
    result={'initial_validation':run['initial_validation'],'best_validation':run['best_validation'],
            'test':run['test'],'scope':'synthetic bands, not real-image recognition accuracy'}
    return emit(result)

if __name__=="__main__":
    main()
