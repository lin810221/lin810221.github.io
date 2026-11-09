"""DFE conversion and synthetic folic-acid UL use different quantities."""
from nutrition_core import folate_dfe
for form in ("food_folate","folic_acid_with_food","folic_acid_empty_stomach"): print(form,folate_dfe(200,form))
try: folate_dfe(200,"5-MTHF")
except ValueError as error: print("Expected rejection:",error)
