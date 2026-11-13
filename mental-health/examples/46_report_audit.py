"""46: report_audit. Original fictional educational example."""
from psych_data import diary_arithmetic,workdays
from psych_core import work_ledger
print(diary_arithmetic()["summary"])
print([work_ledger(d["available_minutes"],d["planned_task_minutes"],d["overhead_minutes"]) for d in workdays()])
