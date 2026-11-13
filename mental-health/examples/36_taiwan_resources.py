"""36: taiwan_resources. Original fictional educational example."""
from psych_data import DATA
import json
for source in json.loads((DATA/"sources.json").read_text(encoding="utf-8")):
    if "Taiwan" in source["name"]:print(source)
print("2026方案資格、費用和名額需向官方與機構確認；不是自動資格判定。")
