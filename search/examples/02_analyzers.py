"""Word tokens and overlapping Han bigrams are different analyzer choices."""
from search_core import tokenize,han_bigrams

if __name__ == "__main__":
    text = "USB-C AX-100 全文搜尋"
    print("Unicode words:",tokenize(text))
    print("Han bigrams:",han_bigrams(text))
    print("Neither analyzer is an LLM tokenizer or a complete Chinese segmenter.")
