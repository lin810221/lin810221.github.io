"""09: weight-trend. Fictional offline educational example."""
from metabolic_core import rolling,describe
values=[70,70.4,69.9,None,70.1,69.8,70]
print(describe(values))
print(rolling(values,3))
print("短期水分與缺值不轉成脂肪變化或理想體重。")
