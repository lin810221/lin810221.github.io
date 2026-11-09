"""05: lever-arm. Offline fictional educational example."""
from training_core import torque
for arm in (.1,.2,.3):print(arm,torque(100,arm,90))
print("相同外力，不同力臂；不能用外在重量直接判組織負荷。")
