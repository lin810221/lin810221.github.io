"""Candidate-order simulation; not a claim about any engine's ANN internals."""
if __name__ == "__main__":
    candidates = [("private",False),("retired",False),("visible-a",True),("visible-b",True),("visible-c",True)]
    k = 2
    exact_eligible = [name for name,allowed in candidates if allowed][:k]
    for budget in (2,3,5):
        post = [name for name,allowed in candidates[:budget] if allowed][:k]
        print("budget",budget,"post-filter",post,"eligible baseline",exact_eligible)
    print("A result count below k does not prove that eligible documents are absent.")
