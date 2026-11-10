"""48: complete-project. Fictional offline educational example."""
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
from reporting import deliver
parser=argparse.ArgumentParser(description="Fictional metabolic observations, not diagnosis")
parser.add_argument("--output",type=Path)
args=parser.parse_args()
if args.output:print(deliver(args.output))
else:
    with TemporaryDirectory(prefix="metabolic-project-") as temp:print(deliver(Path(temp)/"new-report"))
