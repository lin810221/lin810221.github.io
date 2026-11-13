"""38: before_after_arithmetic. Original fictional educational example."""
from ergo_core import moment,mass_force
force=mass_force(5);before=moment(force,.4);after=moment(force,.2)
print({"before_external_nm":before,"after_external_nm":after,"difference_nm":after-before})
print("外力矩減半不代表人體傷害機率減半，也不是已證實的健康因果。")
