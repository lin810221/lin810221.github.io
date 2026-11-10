"""24: shared-decision. Fictional offline educational example."""
from metabolic_core import coverage
print(coverage({"desired_outcome":"documented","options":None,"values":"documented"},["desired_outcome","options","benefits","harms","values","follow_up"]))
print("共同決策需選項與取捨，不由一個百分比自動選藥。")
