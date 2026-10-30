"""First offline retrieval + extractive answer. No API or model download."""
import json
from rag_core import ask

if __name__ == "__main__":
    result = ask("特休申請提前")
    print(json.dumps(result, ensure_ascii=False, indent=2))
