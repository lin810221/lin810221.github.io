"""Inspect exact character budgets, source mappings, and citation existence."""
from rag_core import all_chunks, extractive_answer, pack_context, retrieve, validate_citations

if __name__ == "__main__":
    query = "特休申請提前"
    hits = retrieve(all_chunks(), query)
    for budget in (40, 500):
        context, sources = pack_context(hits, budget)
        result = extractive_answer(query, sources)
        print("budget chars:", budget, "used:", len(context), "status:", result["status"])
        print(result["answer"])
        print("citation IDs exist:", validate_citations(result["answer"], sources))
