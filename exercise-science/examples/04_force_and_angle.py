"""04: force-and-angle. Offline fictional educational example."""
from training_core import torque
for angle in (0,30,60,90):print(angle,torque(100,.3,angle))
print("力矩模型只算外力與簡化力臂，不推關節內力。")
