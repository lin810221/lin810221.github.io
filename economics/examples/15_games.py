"""Pure Nash and isolated interior mixed equilibria in 2x2 games."""
from microeconomics import game
print("Prisoner dilemma",game())
print("Matching pennies",game(((1,-1),(-1,1)),((-1,1),(1,-1))))
print("All payoffs tied",game(((1,1),(1,1)),((1,1),(1,1))))
