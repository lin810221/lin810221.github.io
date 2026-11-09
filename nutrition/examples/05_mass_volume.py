"""Crossing g and mL requires density, even for a beverage."""
from nutrition_core import volume_mass
print(volume_mass(240,"mL","g",1.02))
try: print(volume_mass(240,"mL","g"))
except ValueError as error: print("Expected rejection:",error)
