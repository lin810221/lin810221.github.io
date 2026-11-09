"""Solve a competitive linear market."""
from microeconomics import market
print(market())
print("Demand shift:",market(a=120))
print("Supply shift:",market(c=30))
