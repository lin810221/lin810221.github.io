"""Mass units and nutrient-specific IU are different concepts."""
from nutrition_core import mass,vitamin_d
print(mass(1000,"mg","g"))
print(mass(1000,"ug","mg"))
print(vitamin_d(1000))
