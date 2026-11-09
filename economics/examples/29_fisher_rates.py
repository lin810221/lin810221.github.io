"""Exact Fisher relation and the low-inflation approximation."""
from macroeconomics import fisher
for inflation in (.02,.10,-.01): print(inflation,fisher(.05,inflation))
