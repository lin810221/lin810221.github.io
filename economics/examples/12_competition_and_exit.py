"""Positive production does not imply positive profit."""
from microeconomics import firm
for fixed in (0,100,1000): print(fixed,firm(price=20,fixed=fixed))
