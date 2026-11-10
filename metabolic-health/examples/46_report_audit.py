"""46: report-audit. Fictional offline educational example."""
from metabolic_data import visits,visit_arithmetic,bp_summary
for visit in visits():print(visit_arithmetic(visit))
print({"bp_complete_mean":bp_summary()["complete_mean"],"diagnosis_generated":False})
print("不是所有欄位都已知，不用正常標籤填缺漏。")
