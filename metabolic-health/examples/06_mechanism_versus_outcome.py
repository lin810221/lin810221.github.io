"""06: mechanism-versus-outcome. Fictional offline educational example."""
from metabolic_core import coverage
print(coverage({"biomarker_change":True,"clinical_events":None},["biomarker_change","clinical_events"]))
print("機制或標記變化不能自動填成疾病事件改善。")
