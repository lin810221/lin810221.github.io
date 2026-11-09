"""Inspect partial food-record totals and their missing values before reporting."""
from food_data import diary
for day,record in diary().items():
    print(day,{k:record["nutrients"][k] for k in ("energy_kcal","calcium_mg","free_sugars_g")})
