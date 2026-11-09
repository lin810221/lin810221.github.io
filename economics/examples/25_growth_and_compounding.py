"""Distinguish cumulative growth, annualized growth and doubling time."""
from macroeconomics import growth
for final in (90,100,150,200): print(final,growth(final=final))
