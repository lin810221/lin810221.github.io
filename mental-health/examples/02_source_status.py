"""02: source_status. Original fictional educational example."""
from psych_data import DATA
import json
print(json.dumps(json.loads((DATA/"sources.json").read_text(encoding="utf-8")),ensure_ascii=False,indent=2))
