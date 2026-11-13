"""41: shared_workstation. Original fictional educational example."""
from ergo_core import coverage
print(coverage({"shared_desk":True,"adjustable_seat":True,"individual_setup_confirmed":False,"remote_space":None},["shared_desk","adjustable_seat","individual_setup_confirmed","remote_space"]))
