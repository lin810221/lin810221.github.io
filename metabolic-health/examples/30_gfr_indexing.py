"""30: gfr-indexing. Fictional offline educational example."""
from metabolic_core import body_surface_area,unindex_gfr
bsa=body_surface_area(170,70)
print({"illustrative_bsa_m2":bsa})
print(unindex_gfr(90,bsa))
print("去指數化不是實測GFR、CKD分期或藥物劑量。")
