"""Word-context counts and positive PMI. No SVD or neural encoder is implied."""
from embedding_core import cooccurrence, ppmi

if __name__ == "__main__":
    vocabulary, counts = cooccurrence("cat eats fish dog eats meat cat likes fish".split(), window=1)
    print("vocabulary:", vocabulary)
    print("counts:")
    for word, row in zip(vocabulary, counts):
        print(word, row)
    print("PPMI:")
    for word, row in zip(vocabulary, ppmi(counts)):
        print(word, [round(x, 3) for x in row])
