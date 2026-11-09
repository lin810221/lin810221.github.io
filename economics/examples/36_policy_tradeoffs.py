"""A higher inflation response changes supply-shock output costs."""
from macroeconomics import is_mp_pc
for response in (0,.5,1,2): print(response,is_mp_pc(phi=response,cost_shock=2))
