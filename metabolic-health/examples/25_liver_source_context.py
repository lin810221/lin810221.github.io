"""25: liver-source-context. Fictional offline educational example."""
import json
from metabolic_data import DATA
print([s for s in json.loads((DATA/"sources.json").read_text(encoding="utf-8"))["baseline"] if s["id"]=="aga2026"])
print("美國路徑、歐洲與土耳其指南不混成台灣規範；TASL不是台灣。")
