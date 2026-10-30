"""Default dry run. --live makes ONE paid embedding request for tiny inputs."""
import argparse
import json
from provider_http import embeddings

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    texts = ["特休申請須提前三個工作日。", "休假要提早多久申請？"]
    if not args.live:
        print(json.dumps({"mode": "dry_run", "endpoint": "POST /v1/embeddings", "model": "text-embedding-3-small", "input": texts}, ensure_ascii=False, indent=2))
        print("To execute: set OPENAI_API_KEY, then pass --live.")
        return
    vectors = embeddings(texts)
    print({"count": len(vectors), "dimensions": len(vectors[0])})

if __name__ == "__main__":
    main()
