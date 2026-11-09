"""38: rolling-missing. Offline fictional educational example."""
from training_core import rolling
print(rolling([200,0,150,None,180,0,200],3))
print("視窗不足或有未知維持None；不把平滑後數值稱恢復分數。")
