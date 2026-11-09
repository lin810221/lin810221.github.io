"""Quote direction, covered parity and the financial-account sign convention."""
from macroeconomics import exchange,balance_of_payments
print(exchange())
print("Domestic depreciation",exchange(spot=35))
print(balance_of_payments())
