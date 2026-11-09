"""Keep per-nutrient unknowns through meal aggregation."""
from food_data import meal
r=meal([{"food_id":"milk","amount":240,"unit":"mL"},{"food_id":"drink","amount":330,"unit":"mL"}])
print(r["nutrients"]["calcium_mg"]);print(r["nutrients"]["sodium_mg"])
