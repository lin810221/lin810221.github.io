"""Offline CLI knowledge assistant. The question is data, never shell code."""
import argparse
import json
from rag_core import ask

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="?", default="國內出差住宿費上限")
    parser.add_argument("--tenant", default="demo", help="Teaching only; production tenant comes from authenticated identity")
    args = parser.parse_args()
    result = ask(args.question, tenant=args.tenant)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
