"""Default dry run; --live makes one external embedding request, possibly paid."""
import argparse
import json
from providers import openai_embeddings, openai_payload

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--dimensions", type=int, default=None)
    args = parser.parse_args()
    texts = ["向量可用來比較表示的方向。", "如何量測兩段文字的相似程度？"]
    if not args.live:
        print(json.dumps({"mode": "dry_run", "endpoint": "POST /v1/embeddings", "payload": openai_payload(texts, dimensions=args.dimensions)}, ensure_ascii=False, indent=2))
        return
    vectors = openai_embeddings(texts, dimensions=args.dimensions)
    print({"count": len(vectors), "dimensions": len(vectors[0])})

if __name__ == "__main__":
    main()
