"""A genuine CPU train/validation loop on a nonlinear synthetic target."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import MLP,make_loaders,train_epoch,evaluate

def main(argv=None):
    del argv
    setup()
    loaders,_=make_loaders('tabular');train,validation,_=loaders
    model=MLP();optimizer=torch.optim.AdamW(model.parameters(),lr=.02)
    initial=evaluate(model,validation);history=[]
    for epoch in range(6):
        training=train_epoch(model,train,optimizer)
        history.append({'epoch':epoch+1,'training':training,'validation':evaluate(model,validation)})
    result={'initial_validation':initial,'history':history,'scope':'synthetic data; test reserved'}
    return emit(result)

if __name__=="__main__":
    main()
