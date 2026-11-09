"""A label serving is not necessarily the amount actually eaten."""
from nutrition_core import serving_label
print(serving_label(per_serving=120,serving_size=250,consumed=500,package_size=500))
