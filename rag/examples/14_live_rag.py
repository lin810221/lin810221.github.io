"""--live: two embedding requests + one Responses request; fictional docs only.

Default is offline. No tools are exposed to the model. Citation-ID validation
does not validate semantic entailment or eliminate prompt injection risk.
"""
import argparse
import json
import os
from provider_http import embeddings, generate
from rag_core import all_chunks, ask, cosine, pack_context, validate_citations, visible

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="?", default="特休申請需要提前幾天？")
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    if not args.live:
        print(json.dumps(ask(args.question), ensure_ascii=False, indent=2))
        print("Offline extractive mode. Set OPENAI_API_KEY and OPENAI_RAG_MODEL, then add --live for real dense RAG.")
        return
    model = os.environ.get("OPENAI_RAG_MODEL")
    if not model:
        raise SystemExit("Set OPENAI_RAG_MODEL to a Responses-compatible model available in your account")
    chunks = visible(all_chunks(), "demo", {"reader"})
    document_vectors = embeddings([chunk.text for chunk in chunks])
    query_vector = embeddings([args.question])[0]
    ranked = sorted(zip(chunks, [cosine(query_vector, v) for v in document_vectors]), key=lambda row: -row[1])[:3]
    context, evidence = pack_context(ranked, budget_chars=1800)
    result = generate(args.question, context, model)
    result["citation_ids_valid"] = validate_citations(result["answer"], evidence)
    if result["status"] == "generated" and not result["citation_ids_valid"]:
        result = {"status": "citation_review_required", "answer": "生成內容未通過引用編號檢查，請人工審核。", "citation_ids_valid": False}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
