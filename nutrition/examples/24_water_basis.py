"""Water changes concentration without necessarily creating nutrients."""
from nutrition_core import cooking
print(cooking(100,250,8,retention=1))
print("Hypothetical nutrient loss",cooking(100,250,8,retention=.8))
