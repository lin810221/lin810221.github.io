"""48: complete_project. Original fictional educational example."""
from pathlib import Path
from tempfile import TemporaryDirectory
from reporting import deliver
import argparse
parser=argparse.ArgumentParser(description="Fictional offline observation report, no diagnosis")
parser.add_argument("--output",type=Path,help="New output directory; existing directories are not overwritten")
args=parser.parse_args()
if args.output:
    report=deliver(args.output);print(args.output,report["checks"])
else:
    with TemporaryDirectory(prefix="mental-project-") as tmp:
        report=deliver(Path(tmp)/"report");print(report["checks"],report["scope"])
