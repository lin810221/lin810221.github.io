"""Default dry run; --live makes one external batch embedding request."""
import argparse
import json
from providers import gemini_embeddings, gemini_payload

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--task", default="RETRIEVAL_DOCUMENT")
    args = parser.parse_args()
    texts = ["文件向量可以預先計算。", "問題與文件要使用相容的編碼設定。"]
    if not args.live:
        print(json.dumps({"mode": "dry_run", "endpoint": "models/gemini-embedding-001:batchEmbedContents", "payload": gemini_payload(texts, task=args.task)}, ensure_ascii=False, indent=2))
        return
    vectors = gemini_embeddings(texts, task=args.task)
    print({"count": len(vectors), "dimensions": len(vectors[0])})

if __name__ == "__main__":
    main()
