"""Complete offline lexical vector search CLI, with inspectable representation."""
import argparse
import json
from embedding_core import workbench

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="向量 相似度 cosine")
    parser.add_argument("--k", type=int, default=3)
    args = parser.parse_args()
    print(json.dumps(workbench(args.query, args.k), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
