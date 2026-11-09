"""An unmeasured nutrient remains unknown; it is not a zero intake."""
from food_data import diary
for day,record in diary().items(): print(day,record["nutrients"]["vitamin_d_ug"],record["nutrients"]["free_sugars_g"])
