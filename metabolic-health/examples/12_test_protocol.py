"""12: test-protocol. Fictional offline educational example."""
from metabolic_data import visits
print(visits()[0]["context"])
print("空腹、樣本、方法與症狀不完整時，不以一個數字下診斷。")
