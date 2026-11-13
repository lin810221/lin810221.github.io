"""18: skill_preferences. Original fictional educational example."""
from psych_core import coverage
record={"skill":"外部定向","acceptable":True,"want_body_scan":False,"effect":None}
print(coverage(record,["skill","acceptable","want_body_scan","effect"]))
print("不想做某技巧是可尊重的偏好，不能自動歸類抗拒治療。")
