"""Calcium in a fictional fortified drink is product-specific; free sugar can remain unknown."""
from food_data import foods,food_portion
for key in ("milk","soy"):
    r=food_portion(foods()[key],240);print(key,r["nutrients"]["calcium_mg"],r["nutrients"]["free_sugars_g"])
