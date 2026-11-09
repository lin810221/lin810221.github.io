"""Use the actual portion and food matrix, not a food-name promise."""
from food_data import foods,food_portion
for key,amount in (("tofu",120),("egg",100),("soy",240)):
    print(key,food_portion(foods()[key],amount)["nutrients"]["protein_g"])
