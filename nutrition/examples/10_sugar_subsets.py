"""Total sugar cannot uniquely identify free sugar."""
from food_data import foods,free_sugar_known
for key in ("fruit","milk","drink","soy"): print(key,free_sugar_known(foods()[key]))
