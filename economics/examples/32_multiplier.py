"""Taxes and imports leak from the simple expenditure multiplier."""
from macroeconomics import multiplier
for imports in (0,.1,.3): print(imports,multiplier(m=imports))
a=multiplier(G=40); b=multiplier(G=50)
print("Delta output",b["output"]-a["output"])
