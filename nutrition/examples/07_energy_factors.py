"""Available carbohydrate excludes fiber; factors are chosen explicitly."""
from nutrition_core import energy
print(energy())
print("Alternative fiber factor",energy(fiber_factor=0))
