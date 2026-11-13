"""06: hrv_context. Original fictional educational example."""
from psych_core import coverage
print(coverage({"signal":"fictional PPG","posture":"seated","breathing_rate":None},["signal","posture","breathing_rate","recording_length","artifact_method"]))
print("缺少條件不能推定壓力；脈搏變異不無條件等於ECG HRV。")
