"""48: complete_project. Original fictional educational example."""
from pathlib import Path
from tempfile import TemporaryDirectory
from reporting import deliver
import argparse
parser=argparse.ArgumentParser(description="Fictional ergonomic observation report; not a safety certificate")
parser.add_argument("--output",type=Path,help="New output directory only")
args=parser.parse_args()
if args.output:
    report=deliver(args.output);print(args.output,report["checks"])
else:
    with TemporaryDirectory(prefix="ergo-project-") as tmp:
        report=deliver(Path(tmp)/"report");print(report["checks"],report["scope"])
