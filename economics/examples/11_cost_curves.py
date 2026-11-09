"""Read fixed, variable, marginal and average costs."""
from microeconomics import firm
for price in (5,10,20,40): print(price,firm(price=price))
