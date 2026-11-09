"""A bank loan creates a loan asset and deposit liability simultaneously."""
from macroeconomics import bank_loan
r=bank_loan(); print(r)
assert sum(r["assets"].values())==sum(r["liabilities"].values())+r["equity"]
