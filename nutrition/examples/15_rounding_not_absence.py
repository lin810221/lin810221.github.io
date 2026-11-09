"""Mathematical rounding is not the legal zero-label rule."""
from nutrition_core import rounded_interval
print(rounded_interval(0,.1))
print(rounded_interval(2.3,.1))
