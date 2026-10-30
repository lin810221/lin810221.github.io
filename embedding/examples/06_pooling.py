"""Handmade token hidden states demonstrate mask-aware mean pooling."""
from embedding_core import mean_pool

if __name__ == "__main__":
    hidden = [[1., 0.], [0., 1.], [2., -1.]]
    print("masked PAD:", mean_pool(hidden, [1, 1, 0]))
    print("unmasked PAD:", mean_pool(hidden, [1, 1, 1]))
    print("These states are illustrative, not actual Transformer output.")
