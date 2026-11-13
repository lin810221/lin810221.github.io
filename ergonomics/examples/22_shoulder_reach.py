"""22: shoulder_reach. Original fictional educational example."""
from ergo_core import mass_force,moment
for arm in (.15,.3):print(moment(mass_force(2),arm,90))
print("只比較外物力矩，不能由此算肩關節內力。")
