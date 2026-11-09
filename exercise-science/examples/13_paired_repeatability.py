"""13: paired-repeatability. Offline fictional educational example."""
from training_core import measurement
from training_data import DATA
import csv
with (DATA/'repeatability.csv').open(encoding='utf-8',newline='') as stream:
    rows=list(csv.DictReader(stream))
print(measurement([float(r['before_cm']) for r in rows],[float(r['after_cm']) for r in rows]))
print("配對重複性示例須檢查系統偏差，不自動判定某人進步。")
