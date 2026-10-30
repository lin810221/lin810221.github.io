"""All prices below are hypothetical; replace them with your current provider rates."""
from decimal import Decimal


def estimate(input_tokens: int, cached_tokens: int, output_tokens: int,
             input_per_million: str, cached_per_million: str, output_per_million: str) -> Decimal:
    tokens = (input_tokens, cached_tokens, output_tokens)
    if any(type(value) is not int or value < 0 for value in tokens) or cached_tokens > input_tokens:
        raise ValueError("Token counts must be nonnegative integers; cached is a subset of input")
    prices = [Decimal(value) for value in (input_per_million, cached_per_million, output_per_million)]
    if any(not price.is_finite() or price < 0 for price in prices):
        raise ValueError("Prices must be finite and nonnegative")
    uncached = input_tokens - cached_tokens
    return (uncached * prices[0] + cached_tokens * prices[1] + output_tokens * prices[2]) / Decimal(1_000_000)


if __name__ == "__main__":
    print("假設價格，非任何供應商報價：")
    print(estimate(10000, 6000, 1000, "2", "0.5", "8"))
