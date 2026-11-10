"""02: source-status. Fictional offline educational example."""
import json
from metabolic_data import DATA
print(json.loads((DATA/"sources.json").read_text(encoding="utf-8")))
print("正式發布、草案與已公告未生效分開保存。")
