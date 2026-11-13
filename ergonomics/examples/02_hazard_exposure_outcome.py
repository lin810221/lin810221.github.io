"""02: hazard_exposure_outcome. Original fictional educational example."""
from ergo_core import coverage
record={"hazard":"repeated reach","duration_minutes":30,"symptoms":None,"diagnosis":None}
print(coverage(record,["hazard","duration_minutes","symptoms","diagnosis"]))
print("危害、暴露、感受與診斷分開，未知不補正常。")
