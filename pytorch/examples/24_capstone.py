"""Train, validate, checkpoint and predict. Default artifacts live in a temporary folder."""
import argparse
import json
from pathlib import Path
import tempfile
from course_core import Config, experiment, load_checkpoint, predict, save_checkpoint

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs",type=int,default=10)
    parser.add_argument("--device",choices=["cpu","cuda","auto"],default="cpu")
    parser.add_argument("--output",type=Path,help="Optional new checkpoint filename; existing files are preserved")
    args = parser.parse_args(argv)
    if args.output and args.output.exists():
        parser.error("Choose a new output filename")
    run = experiment(Config(epochs=args.epochs),device=args.device)
    if args.output:
        save_checkpoint(args.output,run["checkpoint"])
        restored = load_checkpoint(args.output)
    else:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"capstone.pt"
            save_checkpoint(path,run["checkpoint"])
            restored = load_checkpoint(path)
    result = {"torch_baseline":restored["torch_version"],"epochs":restored["epoch"],
              "initial_validation":run["initial_validation"],"final_validation":run["final_validation"],
              "test_of_best_validation_model":run["test"],"prediction":predict(restored,[[0.,0.,0.,0.]]),
              "saved_to":str(args.output) if args.output else "temporary directory, removed after demonstration",
              "data":"synthetic; no production accuracy claim"}
    print(json.dumps(result,indent=2))
    return result

if __name__ == "__main__":
    main()
