## 什麼時候需要動態流程

簡單問題通常一次檢索就足夠。複雜問題可能需要把題目拆開、比對不同資料、發現不足後再搜尋。Agentic RAG 把「接下來要找什麼」交給受控的決策流程，允許多輪工具使用。

多跑幾輪本身不是品質保證。它也可能重複搜尋、偏離問題或讓不可靠的中間推論影響後續查詢。因此每次重查都要有明確缺口、成本上限與停止條件。

## 一個可以驗收的狀態

```python
from typing import TypedDict

class RAGState(TypedDict):
    question: str
    tenant: str
    roles: list[str]
    queries: list[str]
    evidence_ids: list[str]
    missing_aspects: list[str]
    attempts: int
    answer: str
```

tenant 和 roles 由外部身分驗證設定，不交給模型任意修改。每輪候選重新套用授權。衍生查詢與證據分開保存，中間草稿不能被誤認為新文件。

## 用 LangGraph 描述控制流

```text
START → classify → retrieve → assess
                         ↙       ↘
          rewrite → retrieve       generate → verify → END
              （最多有限輪）        ↘ review / insufficient_evidence
```

節點各自回傳需要更新的欄位，條件邊決定是否重查。LangGraph 的圖 API 支援明確節點與路由；詳細 reducer、checkpoint 與 interrupt 可接回既有課程。[LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)

## 停止條件應寫在程式裡

例如最多兩次檢索、單輪工具 timeout、總字元或 token 預算、候選集合沒有新增、相同查詢不重跑。若達上限仍不足，回傳缺少面向，而不是假裝完成。

可以讓模型提出 `missing_aspects`，但是否增加權限、花費或執行有副作用工具，仍由應用政策決定。只讀知識助理通常不需要寫檔、寄信或修改資料的工具。

## 評估多步流程

除了最終答案，也記錄工具呼叫數、每輪新增有效證據、重查比例、超出預算率與拒答。若多輪版相對固定流程沒有改善品質，卻大幅增加延遲，就應簡化決策或只對特定題型啟用。

注意 Self-RAG 是一個具體研究方法，包含專門的學習與反思設計；在一般 prompt 裡加「再檢查一次」不能稱為重現該方法。[Self-RAG 論文](https://arxiv.org/abs/2310.11511)

## 練習與答案

**題目：**模型連續產生三個同義查詢，結果都沒有新片段，應繼續嗎？

**參考答案：**到達無新增證據或輪數條件就停止，回報不足或要求澄清。若確認是索引缺文件，應修資料匯入；持續改寫不能補出知識庫不存在的資料。
