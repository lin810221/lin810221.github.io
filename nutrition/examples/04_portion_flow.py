"""A portion is measured in the same basis; not an absorption model."""
from food_data import foods,food_portion
for amount in (50,100,180): print(food_portion(foods()["grain"],amount,"g"))
