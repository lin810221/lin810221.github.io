"""A tax can improve welfare when there is unpriced damage."""
from microeconomics import externality,market
r=externality(); print(r)
print("Pigouvian tax implements optimal Q",market(tax=r["pigou_tax"])["q"])
