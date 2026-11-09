"""20: frequency-volume. Offline fictional educational example."""
plans={"two_days":[4,4],"four_days":[2,2,2,2]}
for name,sets in plans.items():print(name,{"weekly_declared_sets":sum(sets),"days":len(sets)})
print("同總量不同分配，不證明所有其他條件或效果相同。")
