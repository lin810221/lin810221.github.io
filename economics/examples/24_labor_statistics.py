"""An unemployment-rate decline can result from labor-force exit."""
from macroeconomics import labor
print("Before",labor(90,10,150))
print("Five stop searching, no new jobs",labor(90,5,150))
