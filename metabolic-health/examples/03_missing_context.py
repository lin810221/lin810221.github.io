"""03: missing-context. Fictional offline educational example."""
from metabolic_core import coverage
print(coverage({"fasting":None,"symptoms":None,"unit":"mg/dL"},["fasting","symptoms","unit","medications"]))
print("不知道不等於已確認沒有。")
