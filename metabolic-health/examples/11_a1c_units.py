"""11: a1c-units. Fictional offline educational example."""
from metabolic_core import a1c_units
print(a1c_units(6.5))
print(a1c_units(48,"IFCC_mmol_mol"))
print("IFCC mmol/mol不是血糖mmol/L；換算不是確診。")
