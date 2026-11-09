"""Export CSV, standalone SVG and provenance-preserving JSON."""
from pathlib import Path
from tempfile import TemporaryDirectory
import argparse
from reporting import deliver
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
args=parser.parse_args()
if args.output:print(deliver(args.output))
else:
    with TemporaryDirectory() as folder: print(deliver(Path(folder)/'report'))
