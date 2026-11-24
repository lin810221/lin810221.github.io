"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from torch.nn import functional as F
from lm_core import print_json

def main():
    # Sequence log-probabilities are sums over response tokens, prompt excluded.
    policy_chosen=torch.tensor(-2.,requires_grad=True);policy_rejected=torch.tensor(-4.,requires_grad=True)
    reference_chosen,reference_rejected=-3.,-4.
    beta=.2
    margin=beta*((policy_chosen-policy_rejected)-(reference_chosen-reference_rejected))
    loss=-F.logsigmoid(margin);loss.backward()
    print_json({'margin':float(margin.detach()),'loss':float(loss.detach()),
        'chosen_gradient':float(policy_chosen.grad),'rejected_gradient':float(policy_rejected.grad),
        'scope':'original scalar objective, no real preference training or alignment guarantee'})

if __name__=='__main__':main()
