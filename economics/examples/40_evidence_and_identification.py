"""OLS association and a two-by-two DID are not automatic causal proof."""
from evidence import ols,difference_in_differences
print(ols([1,2,3,4],[3,5,7,9]))
print(difference_in_differences(100,115,80,90))
