"""Strict application-level validation after JSON decoding. No provider call."""
from contracts import ANSWER_SCHEMA, Answer, validate_answer


if __name__ == "__main__":
    result = validate_answer('{"answer":"Agent 透過工具執行工作。","sources":["D1"]}', {"D1"})
    print(result)
