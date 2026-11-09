"""Percentage points and percent changes are different units."""
from macroeconomics import percent_change
print({"index_100_to_105_percent":percent_change(100,105),"rate_4_to_5_change_pp":5-4,"rate_relative_change_percent":percent_change(4,5)})
