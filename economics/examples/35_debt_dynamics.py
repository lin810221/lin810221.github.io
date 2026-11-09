"""Net debt ratio uses matched nominal interest and nominal GDP growth."""
from macroeconomics import debt_path
for interest in (.02,.04,.06):
    r=debt_path(nominal_interest=interest,periods=10); print(interest,r["stabilizing_primary_surplus"],r["rows"][-1])
