"""16: relative-load. Offline fictional educational example."""
from training_core import relative_load
for weight in (40,60,80):print(weight,relative_load(weight,80))
print("80kg為假設參考，%1RM不是RPE，也不能保證固定可做次數。")
