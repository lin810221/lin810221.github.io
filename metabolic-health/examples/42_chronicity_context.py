"""42: chronicity-context. Fictional offline educational example."""
from metabolic_core import coverage
print(coverage({"single_eGFR":60,"prior_records":None,"albuminuria":None},["single_eGFR","prior_records","albuminuria","clinical_context"]))
print("慢性證據與急性評估不同；不是一律等三個月才處理。")
