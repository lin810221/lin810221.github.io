"""Genuine gradient updates on six words; not a pretrained semantic encoder."""
from embedding_core import tiny_skipgram

if __name__ == "__main__":
    result = tiny_skipgram()
    print("initial loss:", result["initial_loss"])
    print("final loss:", result["final_loss"])
    print("tiny target vectors:")
    for word, values in result["target_vectors"].items():
        print(word, [round(x, 4) for x in values])
    print("Loss decrease shows fitting these labels, not general language understanding.")
