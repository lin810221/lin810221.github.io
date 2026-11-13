"""27: organizational_actions. Original fictional educational example."""
from psych_core import coverage
record={"individual_action":"可選休息","team_action":"重新協調優先序","organization_action":"評估人力與工時","implemented":None}
print(record,coverage(record,["individual_action","team_action","organization_action","implemented"]))
