"""Read an invented food with explicit units, state and source."""
from food_data import foods,food_portion
f=foods()["grain"]; print(f)
print(food_portion(f,150,"g"))
