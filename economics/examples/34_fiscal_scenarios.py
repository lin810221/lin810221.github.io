"""Compare spending and lump-sum tax changes in the same fixed-price model."""
from macroeconomics import multiplier
base=multiplier(); spend=multiplier(G=50); tax=multiplier(T0=-10)
print({"baseline":base,"spending10":spend,"tax_cut10":tax})
