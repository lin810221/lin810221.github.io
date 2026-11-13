"""44: screening_bayes. Original fictional educational example."""
from psych_data import DATA
from psych_core import screening
import csv
with (DATA/"screening_cases.csv").open(encoding="utf-8",newline="") as stream:
    for row in csv.DictReader(stream):print(screening(int(row["population"]),float(row["prevalence"]),float(row["sensitivity"]),float(row["specificity"])))
