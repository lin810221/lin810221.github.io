"""22: risk-baselines. Fictional offline educational example."""
from metabolic_core import assumed_effect
for baseline in (.1,.01):print(assumed_effect(baseline,.8))
print("固定假設RR不保證能外推所有族群；此處不計個人PREVENT風險。")
