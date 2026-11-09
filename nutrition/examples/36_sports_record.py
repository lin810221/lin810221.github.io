"""A training-day food record describes intake, not a validated athlete prescription."""
from food_data import meal
r=meal([{"food_id":"milk","amount":240},{"food_id":"fruit","amount":150},{"food_id":"nuts","amount":20}]);print(r["nutrients"]["protein_g"],r["nutrients"]["available_carb_g"])
