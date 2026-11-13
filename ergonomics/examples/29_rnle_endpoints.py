"""29: rnle_endpoints. Original fictional educational example."""
from ergo_core import rnle
origin=rnle(h_cm=25,v_cm=75,d_cm=50);destination=rnle(h_cm=40,v_cm=125,d_cm=50)
print({"origin":origin,"destination":destination,"lower_rwl_if_both_endpoints_required":min(origin["rwl_kg"],destination["rwl_kg"])})
print("目的地需顯著控制時檢查兩端；不是把LI取平均成CLI。")
