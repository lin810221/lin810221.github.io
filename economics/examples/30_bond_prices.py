"""Fixed annual cash flows, prices and duration; not an investment recommendation."""
from macroeconomics import bond,present_value
for rate in (.02,.04,.08): print(rate,bond(yield_rate=rate))
print("Project NPV",present_value())
