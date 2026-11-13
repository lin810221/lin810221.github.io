"""01: task_person_environment. Original fictional educational example."""
from ergo_core import coverage
record={"task":"fictional desk task","person_needs":None,"environment":"adjustable setup","synthetic":True}
print(record,coverage(record,["task","person_needs","environment","synthetic"]))
