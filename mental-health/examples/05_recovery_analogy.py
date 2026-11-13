"""05: recovery_analogy. Original fictional educational example."""
from psych_core import recovery_analogy
for retention in (.4,.8):
    model=recovery_analogy(10,retention)
    print(retention,model["rows"][-1],model["scope"])
