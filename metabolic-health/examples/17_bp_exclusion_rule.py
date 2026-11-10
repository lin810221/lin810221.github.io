"""17: bp-exclusion-rule. Fictional offline educational example."""
from metabolic_data import bp_summary
for rule in (False,True):
    r=bp_summary(exclude_first_day=rule)
    print({"exclude_first_day":rule,"expected":r["expected_pairs"],"observed":r["observed_pairs"],"available_mean":r["available_mean"]})
print("明示比較規則，不選較好看的平均作診斷。")
