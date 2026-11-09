"""Ingredient lists cannot fully describe shared-equipment exposure."""
records=[{"food":"A","ingredient_allergen":False,"shared_equipment":"unknown"},{"food":"B","ingredient_allergen":True,"shared_equipment":"known"}]
for row in records:print(row)
print("This is a record schema, not a diagnostic classifier.")
