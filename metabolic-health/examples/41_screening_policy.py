"""41: screening-policy. Fictional offline educational example."""
from metabolic_core import coverage
print(coverage({"jurisdiction":"Taiwan","benefit_policy":"2025 expansion","personal_follow_up":None},["jurisdiction","benefit_policy","personal_follow_up","symptoms","previous_results"]))
print("公費服務頻率不等於異常檢驗應等到下一次公費週期。")
