"""09: rumination_and_action. Original fictional educational example."""
from psych_core import coverage
for record in [{"question":"我怎麼總是這樣","next_action":None},{"question":"明天需先確認哪件事","next_action":"詢問截止時間"}]:
    print(record,coverage(record,["question","next_action"]))
