"""Application output contract. Schema validity alone does not prove factual support."""
import json
import re
from dataclasses import dataclass

ANSWER_SCHEMA = {
    "type": "object",
    "properties": {"answer": {"type": "string"}, "sources": {"type": "array", "items": {"type": "string"}}},
    "required": ["answer", "sources"], "additionalProperties": False,
}


@dataclass(frozen=True)
class Answer:
    answer: str
    sources: tuple[str, ...]


def validate_answer(raw: str, allowed_ids: set[str]) -> Answer:
    data = json.loads(raw)
    if not isinstance(data, dict) or set(data) != {"answer", "sources"}:
        raise ValueError("Expected exactly answer and sources")
    if not isinstance(data["answer"], str) or not data["answer"].strip():
        raise ValueError("answer must be a nonempty string")
    sources = data["sources"]
    if not isinstance(sources, list) or not sources or any(not isinstance(item, str) for item in sources):
        raise ValueError("sources must be a nonempty string list")
    if len(set(sources)) != len(sources) or not set(sources).issubset(allowed_ids):
        raise ValueError("Sources must be unique retrieved IDs")
    cited = set(re.findall(r"\[(D\d+)\]", data["answer"]))
    if not cited.issubset(set(sources)):
        raise ValueError("Inline citations must be declared in sources")
    return Answer(data["answer"], tuple(sources))
