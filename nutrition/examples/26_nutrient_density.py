"""Per100kcal is one lens, not a whole-food health score."""
from food_data import foods
from nutrition_core import density_per_100kcal
for key in ("tofu","milk","nuts"):
    v=foods()[key]["nutrients"]; print(key,density_per_100kcal(v["calcium_mg"],v["energy_kcal"]))
