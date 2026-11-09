"""Solve three static equations; rates and gaps are in percentage points."""
from macroeconomics import is_mp_pc
print("Baseline",is_mp_pc())
print("Demand shock",is_mp_pc(a=2))
print("Supply shock",is_mp_pc(cost_shock=2))
