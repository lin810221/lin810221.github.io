"""22: estimated-one-rm. Offline fictional educational example."""
from training_core import estimated_1rm
for formula in ("epley","brzycki"):print(formula,estimated_1rm(60,5,formula))
print("公式差異是模型不確定；沒有實測最大能力或要求你測最大重量。")
