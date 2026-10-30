"""A deterministic follow-up resolver. Ambiguity is made explicit."""
from rag_core import ask

def resolve(question, topic):
    if "那" in question and not topic:
        return None
    return f"{topic} {question}" if "那" in question else question

if __name__ == "__main__":
    topic = "遠端工作"
    followup = "那每週最多幾日？"
    standalone = resolve(followup, topic)
    print("resolved query:", standalone)
    print(ask(standalone)["answer"] if standalone else "請先說明你指的是哪一項規範。")
