"""Learn vocabulary/IDF on documents, reuse it for queries. Lexical baseline."""
from embedding_core import Tfidf

if __name__ == "__main__":
    encoder = Tfidf().fit(["apple apple fruit", "banana fruit", "database sql"])
    print("vocabulary:", encoder.vocabulary)
    print("idf:", encoder.idf)
    print("query:", encoder.transform("apple fruit"))
    print("unknown:", encoder.transform("unseenword"))
