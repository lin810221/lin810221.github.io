"""08: pressure_and_area. Original fictional educational example."""
from ergo_core import contact_pressure,normal_stress
print(contact_pressure(200,100));print(normal_stress(100,50))
print("接觸面積cm²與材料截面mm²不同，不推組織安全界線。")
