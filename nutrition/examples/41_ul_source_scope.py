"""Synthetic folic acid is not total food folate or DFE for this US UL."""
from nutrition_core import scoped_total,reference_percent
from food_data import references
rows=[{"name":"food folate","amount":400,"source_type":"natural_food"},{"name":"folic acid","amount":400,"source_type":"supplement"}]
r=scoped_total(rows,{"supplement","fortified_folic_acid"});print(r)
print(reference_percent(r["amount"],"ug",references()["us_folic_acid_ul"],form="folic_acid",source_scope="supplements_and_fortification"))
