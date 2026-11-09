"""Equalize marginal abatement cost subject to capacity limits."""
from microeconomics import abatement
for target in (0,12,20,25): print(target,abatement(target))
