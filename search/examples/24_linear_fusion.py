"""Per-query min-max normalization is a policy, not probability calibration."""
from search_core import linear_fusion

if __name__ == "__main__":
    lexical = [(1,20.0),(2,5.0),(3,1.0)]
    dense = [(2,0.91),(1,0.90),(4,0.88)]
    for weights in ([0.8,0.2],[0.2,0.8]): print(weights,linear_fusion([lexical,dense],weights))
    print("Constant-score branches contribute zero discrimination in this implementation.")
