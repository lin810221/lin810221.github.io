"""Verify the private surplus plus tax revenue accounting identity."""
from microeconomics import market
for tax in (0,10,20,40):
    r=market(tax=tax); print(tax,r)
    assert abs(r["cs"]+r["ps"]+r["revenue"]-r["total_surplus"])<1e-9
