"""Train a nonlinear MLP on all four XOR corners; training sanity only."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    x=torch.tensor([[0.,0.],[0.,1.],[1.,0.],[1.,1.]])
    y=torch.tensor([[0.],[1.],[1.],[0.]])
    model=nn.Sequential(nn.Linear(2,8),nn.Tanh(),nn.Linear(8,1))
    optimizer=torch.optim.Adam(model.parameters(),lr=.05)
    initial=F.binary_cross_entropy_with_logits(model(x),y).item()
    for _ in range(350):
        optimizer.zero_grad(set_to_none=True)
        loss=F.binary_cross_entropy_with_logits(model(x),y)
        loss.backward();optimizer.step()
    with torch.inference_mode():probability=model(x).sigmoid()
    result={'initial_bce':initial,'final_bce':loss.item(),'probabilities':probability,
            'predictions':(probability>=.5).long(),'scope':'four training points, no generalization claim'}
    return emit(result)

if __name__=="__main__":
    main()
