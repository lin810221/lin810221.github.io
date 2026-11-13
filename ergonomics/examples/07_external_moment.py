"""07: external_moment. Original fictional educational example."""
from ergo_core import mass_force,moment
force=mass_force(10)
for radius in (.2,.4):print(radius,moment(force,radius,90))
print("外力矩不是腰椎壓力、肌腱力或傷害機率。")
