"""45: effects_and_causality. Original fictional educational example."""
from psych_core import standardized_difference,paired_association
print(standardized_difference())
print(paired_association([1,2,None,4],[4,3,2,1]))
print("相關非因果，SMD不是個人改善或臨床重要差。")
