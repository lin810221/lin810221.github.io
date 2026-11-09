"""Income and substitution can both change desired work hours."""
from microeconomics import leisure
for wage in (5,10,20): print(wage,leisure(wage=wage))
print("Large nonlabor income corner",leisure(nonlabor=1000))
