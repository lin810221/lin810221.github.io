"""Controlled domain vocabulary; expanded text is a query, never evidence."""
from rag_core import all_chunks, retrieve, rrf

SYNONYMS = {"休假": "特休 申請", "住飯店": "住宿費 上限", "連不上": "VPN 故障 錯誤碼"}

def variants(query):
    return list(dict.fromkeys([query] + [query.replace(word, expansion) for word, expansion in SYNONYMS.items() if word in query]))

if __name__ == "__main__":
    query = "出差住飯店的額度"
    print("variants:", variants(query))
    hits = rrf([retrieve(all_chunks(), variant) for variant in variants(query)])
    print([(chunk.doc_id, round(score, 6)) for chunk, score in hits])
