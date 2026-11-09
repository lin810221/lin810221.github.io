"""Portion uncertainty produces deterministic bounds, not a confidence interval."""
from nutrition_core import interval_sum
print(interval_sum([116,80],[(120,180),(80,120)]))
