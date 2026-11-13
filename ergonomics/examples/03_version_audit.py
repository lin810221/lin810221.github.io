"""03: version_audit. Original fictional educational example."""
from ergo_data import DATA
import json
print(json.dumps(json.loads((DATA/"references.json").read_text(encoding="utf-8")),ensure_ascii=False,indent=2))
