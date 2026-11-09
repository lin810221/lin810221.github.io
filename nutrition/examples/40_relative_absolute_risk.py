"""Relative reductions must be read with absolute risk and horizon."""
from nutrition_core import risk_comparison
print(risk_comparison(1,100,2,100))
print(risk_comparison(100,1000,200,1000))
