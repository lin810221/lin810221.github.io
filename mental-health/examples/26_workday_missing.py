"""26: workday_missing. Original fictional educational example."""
from psych_data import workdays
from psych_core import work_ledger
for day in workdays():print(day["id"],work_ledger(day["available_minutes"],day["planned_task_minutes"],day["overhead_minutes"]))
