"""Default explains the opt-in; --compile --backend eager tests graph capture."""
import argparse
import json
import torch
from course_core import TinyMLP, setup

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compile",action="store_true")
    parser.add_argument("--backend",choices=["eager","inductor"],default="eager")
    args = parser.parse_args(argv)
    if not args.compile:
        result = {"mode":"eager_baseline","next":"Add --compile --backend eager to check capture; inductor needs a compatible toolchain"}
    else:
        setup()
        model = TinyMLP(dropout=0).eval()
        sample = torch.randn(2,4)
        compiled = torch.compile(model,backend=args.backend,fullgraph=True)
        with torch.inference_mode():
            error = (compiled(sample)-model(sample)).abs().max().item()
        result = {"backend":args.backend,"maximum_error":error,
                  "scope":"eager backend checks graph capture, not optimized performance"}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
