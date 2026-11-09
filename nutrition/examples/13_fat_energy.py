"""Fat grams and percentage of total energy use different denominators."""
from nutrition_core import energy_percent
for total in (1600,2000,2400): print(total,energy_percent(20,9,total))
