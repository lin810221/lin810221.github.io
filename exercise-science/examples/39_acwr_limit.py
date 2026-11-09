"""39: acwr-limit. Offline fictional educational example."""
from training_core import load_ratio
print(load_ratio(1100,[900,1000,1100,1000]))
print(load_ratio(1100,[900,None,1100,1000]))
print("current不混入四週基線；比值只是描述，沒有安全區或傷害機率。")
