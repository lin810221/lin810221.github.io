"""Variable-length GRU classification on a known last-token rule."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import experiment

def main(argv=None):
    del argv
    setup()
    run=experiment('sequence')
    result={'initial_validation':run['initial_validation'],'best_validation':run['best_validation'],'test':run['test'],
            'scope':'target is last token >=5; a direct rule is a perfect baseline, GRU is an implementation exercise'}
    return emit(result)

if __name__=="__main__":
    main()
