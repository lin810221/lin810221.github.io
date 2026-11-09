"""47: report-preview. Offline fictional educational example."""
from tempfile import TemporaryDirectory
from pathlib import Path
from reporting import deliver
with TemporaryDirectory(prefix="exercise-preview-") as temp:
    print(deliver(Path(temp)/"new-report"))
print("預覽暫存檔會清除；保留報告請用48入口的--output新目錄。")
