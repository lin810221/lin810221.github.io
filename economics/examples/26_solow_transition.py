"""Discrete per-effective-worker capital transition and steady state."""
from macroeconomics import solow
r=solow(periods=60); print({k:v for k,v in r.items() if k!="path"})
for row in r["path"][::10]: print(row)
