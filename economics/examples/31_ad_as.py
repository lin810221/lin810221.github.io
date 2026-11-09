"""Aggregate price-level and output movements in a static linear illustration."""
from macroeconomics import ad_as
print("Baseline",ad_as())
print("Demand expansion",ad_as(A=220))
print("Adverse supply shift",ad_as(C=0))
