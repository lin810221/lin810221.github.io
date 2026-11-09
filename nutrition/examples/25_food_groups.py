"""Group presence is a description, not proof a day is balanced."""
from food_data import meal
print(meal([{ "food_id":"grain","amount":150,"unit":"g"},{"food_id":"tofu","amount":120,"unit":"g"},{"food_id":"vegetable","amount":180,"unit":"g"}])["groups_present"])
