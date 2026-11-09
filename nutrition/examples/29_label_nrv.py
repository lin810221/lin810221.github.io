"""Authentic Taiwan label references; sugars and trans-fat NRVs are not invented."""
from food_data import references
from nutrition_core import reference_percent
r=references()
print(reference_percent(400,"mg",r["tw_label_sodium"]))
print(reference_percent(10,"g",r["tw_label_sugars"]))
