"""Fixed-base teaching data; official chained volumes are generally non-additive."""
from evidence import read_basket
from macroeconomics import price_indexes
data=read_basket(); base=data["2024"]; items=sorted(base)
for period,rows in sorted(data.items()):
    print(period,price_indexes([base[i]["price"] for i in items],[base[i]["quantity"] for i in items],[rows[i]["price"] for i in items],[rows[i]["quantity"] for i in items]))
