"""Separate legal payment, economic incidence and rationing assumptions."""
from microeconomics import market,price_control
for tax in (0,20,80,100): print("tax",tax,market(tax=tax))
print("ceiling, efficient rationing assumed",price_control(40))
print("floor, efficient rationing assumed",price_control(80,"floor"))
