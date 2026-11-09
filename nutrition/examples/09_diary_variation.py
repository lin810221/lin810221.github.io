"""Partial records and repeated-day means do not diagnose adequacy."""
from food_data import diary
from nutrition_core import repeated_days
rows=diary()
print(repeated_days([row["nutrients"]["energy_kcal"]["amount"] for row in rows.values()]))
