"""21: lipid-specific-units. Fictional offline educational example."""
from metabolic_core import concentration
for analyte in ("cholesterol","triglycerides"):
    print(analyte,concentration(150,analyte))
try:concentration(50,"lp_a")
except ValueError as error:print(error)
print("Lp(a)沒有通用質量／莫耳固定換算係數。")
