"""33: care_options_context. Original fictional educational example."""
from psych_core import coverage
record={"goal":"改善生活功能","preferences":None,"previous_response":None,"risks_discussed":False}
print(coverage(record,["goal","preferences","previous_response","risks_discussed"]))
