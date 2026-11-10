"""23: prevent-age-scope. Fictional offline educational example."""
from metabolic_core import prevent_age_scope
for age,horizon in [(45,10),(65,10),(65,30),(80,10)]:print(age,prevent_age_scope(age,horizon))
print("只查年齡範圍，不是完整資格判定或台灣校準模型。")
