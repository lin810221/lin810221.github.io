"""09: relaxation_analogy. Original fictional educational example."""
from ergo_core import relaxation_analogy
for tau in (5,15):
    model=relaxation_analogy(tau=tau);print(tau,model["rows"][-1],model["scope"])
