"""47: report-preview. Fictional offline educational example."""
from pathlib import Path
from tempfile import TemporaryDirectory
from reporting import deliver
with TemporaryDirectory(prefix="metabolic-preview-") as temp:print(deliver(Path(temp)/"new-report"))
print("暫存預覽結束清除；保留報告用48入口的--output新目錄。")
