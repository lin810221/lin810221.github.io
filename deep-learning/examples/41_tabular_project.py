"""A nonlinear tabular MLP with train-only scaling and best-validation selection."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import experiment

def main(argv=None):
    del argv
    setup()
    run=experiment('tabular')
    result={'initial_validation':run['initial_validation'],'best_validation':run['best_validation'],
            'test':run['test'],'last_epoch':run['history'][-1],
            'scope':'synthetic nonlinear rule; test evaluates the validation-selected model'}
    return emit(result)

if __name__=="__main__":
    main()
