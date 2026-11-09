"""Reported energy and a selected-factor reconstruction need not be identical."""
from food_data import foods
from nutrition_core import energy
f=foods()["milk"]["nutrients"]
reconstructed=energy(f["available_carb_g"],f["protein_g"],f["fat_g"],f["fiber_g"])["kcal"]
print({"reported_kcal":f["energy_kcal"],"selected_factor_kcal":reconstructed,"not_a_compliance_test":True})
