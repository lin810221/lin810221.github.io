"""18: volume-load. Offline fictional educational example."""
from training_core import volume
print(volume([{"reps":8,"load_kg":40}]*3))
print(volume([{"reps":8,"load_kg":None}]))
print("3x8x40=960kg-reps；不是J，也不代表相同肌肉刺激。")
