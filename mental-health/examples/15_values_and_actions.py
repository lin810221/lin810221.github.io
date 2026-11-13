"""15: values_and_actions. Original fictional educational example."""
from psych_core import coverage
record={"value":"尊重合作","small_action":"會議前確認一項需求","outcome_guarantee":None}
print(record,coverage(record,["value","small_action","outcome_guarantee"]))
