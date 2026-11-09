"""Compare two fictional meal structures without optimizing a person."""
from food_data import meal
for items in ([{"food_id":"grain","amount":180},{"food_id":"tofu","amount":120},{"food_id":"vegetable","amount":180}], [{"food_id":"grain","amount":180},{"food_id":"egg","amount":100}]):
    r=meal(items);print(r["groups_present"],r["nutrients"]["fiber_g"])
