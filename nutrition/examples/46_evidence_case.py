"""A fictional risk calculation cannot validate a nutrition claim by itself."""
from nutrition_core import risk_comparison
print(risk_comparison(8,1000,10,1000))
print("Need outcome, horizon, comparator, population, confidence and conflicts of interest.")
