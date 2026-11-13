"""24: repeated_task_record. Original fictional educational example."""
from ergo_data import observations
from ergo_core import repetition
for row in observations()[:3]:print(row["id"],repetition(row["actions"],row["scheduled_minutes"],row["active_minutes"]))
