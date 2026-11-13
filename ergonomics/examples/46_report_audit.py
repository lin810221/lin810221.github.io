"""46: report_audit. Original fictional educational example."""
from ergo_data import observation_summary,workers,lift_cases
from ergo_core import population_fit,rnle
print(observation_summary());print(population_fit(workers()));print([rnle(**case["inputs"]) for case in lift_cases()])
