"""Compare composition on explicit cooked/edible bases."""
from food_data import foods,food_portion
for key in ("grain","vegetable","fruit"): print(key,foods()[key]["state"],food_portion(foods()[key],150,"g")["nutrients"]["fiber_g"])
