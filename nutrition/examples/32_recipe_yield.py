"""Explicit yield and retention do not replace a measured cooked composition."""
from nutrition_core import cooking
for retention in (1,.8,.5): print(cooking(200,500,10,retention))
