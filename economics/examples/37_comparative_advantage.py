"""World price between opportunity costs is necessary, not every trade volume benefits both."""
from microeconomics import trade
for volume in (10,30,50): print(volume,trade(export_x=volume))
