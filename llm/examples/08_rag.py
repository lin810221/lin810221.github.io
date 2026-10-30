"""Traceable retrieval baseline without embeddings or provider calls."""
from knowledge import retrieve, extractive_answer

if __name__ == "__main__":
    for question in ["AI Agent 如何使用工具？", "推薦今天的午餐"]:
        result = extractive_answer(retrieve(question))
        print(question, result)
