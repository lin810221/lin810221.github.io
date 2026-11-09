"""Expected log utility and actuarially fair insurance."""
from microeconomics import insurance
for premium in (8,10,20): print(premium,insurance(premium=premium))
