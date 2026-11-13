"""16: seat_desk_context. Original fictional educational example."""
from ergo_core import coverage
print(coverage({"foot_support":True,"clearance_checked":False,"elbow_height_cm":None},["foot_support","clearance_checked","elbow_height_cm","task_height_cm"]))
print("未檢查是已知狀態，不是檢查通過。")
