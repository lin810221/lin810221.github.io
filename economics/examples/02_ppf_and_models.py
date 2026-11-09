"""Compare a frontier, efficient points and marginal opportunity costs."""
from microeconomics import ppf
for x in (20,40,60,80):
    r=ppf(x); print(r, "feasible inside:", r["y"]-10)
