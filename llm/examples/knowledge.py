"""Tiny keyword corpus. Not semantic retrieval, not an embedding model."""
DOCUMENTS = [
    {"id": "D1", "keys": ["agent", "代理", "工具", "自主"],
     "text": "AI Agent 可以由模型決定下一個工具或步驟；應用負責驗證、執行工具與控制停止條件。"},
    {"id": "D2", "keys": ["記憶", "memory", "歷史", "session"],
     "text": "對話歷史、工作狀態與使用者偏好是不同資料；持久記憶需要由應用保存並依使用者範圍讀取。"},
    {"id": "D3", "keys": ["審核", "核准", "approval", "權限"],
     "text": "人工審核應綁定具體動作和內容版本；核准後的執行仍需檢查權限與冪等性。"},
]


def retrieve(question: str) -> list[dict]:
    query = question.casefold().strip()
    return [dict(doc) for doc in DOCUMENTS if any(key in query for key in doc["keys"])]


def extractive_answer(docs: list[dict]) -> dict:
    if not docs:
        return {"status": "insufficient_evidence", "answer": "目前文件沒有足夠依據。", "sources": []}
    return {"status": "draft", "answer": "\n".join(f"{doc['text']} [{doc['id']}]" for doc in docs),
            "sources": [doc["id"] for doc in docs]}
