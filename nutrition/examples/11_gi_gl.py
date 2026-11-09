"""GI is supplied from a study, never inferred from a sugar label."""
from nutrition_core import glycemic_load
for grams in (15,30,60): print(grams,glycemic_load(55,grams))
print("Unknown GI",glycemic_load(None,30))
