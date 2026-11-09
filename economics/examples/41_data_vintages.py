"""Use only information released by the decision date."""
from evidence import read_vintages,as_of
rows=read_vintages()
for cutoff in ("2025-05-01","2025-08-01","2026-02-01"): print(cutoff,as_of(rows,cutoff))
