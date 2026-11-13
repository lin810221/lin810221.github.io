"""47: report_preview. Original fictional educational example."""
from pathlib import Path
from tempfile import TemporaryDirectory
from reporting import deliver
with TemporaryDirectory(prefix="ergo-preview-") as tmp:
    report=deliver(Path(tmp)/"report");print(report["checks"],report["scope"])
