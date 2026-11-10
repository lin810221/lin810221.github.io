"""43: screening-bayes. Fictional offline educational example."""
import csv
from metabolic_data import DATA
from metabolic_core import screening
with (DATA/"screening_cases.csv").open(encoding="utf-8",newline="") as stream:
    for row in csv.DictReader(stream):print(row["id"],screening(int(row["population"]),float(row["prevalence"]),float(row["sensitivity"]),float(row["specificity"])))
print("假設母群體和檢驗性能；陽性不是自動確診。")
