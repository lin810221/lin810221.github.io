"""40: life-stage-context. Fictional offline educational example."""
contexts=["child_adolescent","pregnant_postpartum","older_frail","general_adult"]
for context in contexts:print({"population":context,"adult_thresholds_automatically_applicable":False})
print("年齡、孕期與功能改變適用性，不能把一般成人值直接複製。")
