"""Keep source-specific reference metadata separate from food observations."""
from food_data import references
for key,value in references().items(): print(key,value)
