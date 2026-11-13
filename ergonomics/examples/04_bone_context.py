"""04: bone_context. Original fictional educational example."""
from ergo_core import coverage
print(coverage({"tissue":"bone","fracture_history":None,"measurement_method":None},["tissue","fracture_history","measurement_method","clinical_context"]))
print("骨密度、骨結構與骨折風險不是同一測量。")
