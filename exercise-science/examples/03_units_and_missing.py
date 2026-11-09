"""03: units-and-missing. Offline fictional educational example."""
from training_core import weekly_load
print(weekly_load([200,150,0,200,None,0,150]))
print("0是明示休息；None是沒觀察到，兩者不能互換。")
