"""48: complete-project. Offline fictional educational example."""
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
from reporting import deliver
parser=argparse.ArgumentParser(description="Fictional training report, not a personal program")
parser.add_argument("--output",type=Path)
args=parser.parse_args()
if args.output:print(deliver(args.output))
else:
    with TemporaryDirectory(prefix="exercise-project-") as temp:print(deliver(Path(temp)/"new-report"))
