## 日後先查這張參數表

| 參數 | 影響 | 先檢查什麼 |
| --- | --- | --- |
| chunk size／overlap | 證據範圍與重複 | 單位、條件完整性 |
| BM25 k1／b | 詞頻飽和與長度 | tokenizer 與詞彙是否命中 |
| embedding model／dimensions | 語意表示與容量 | query/document 一致性 |
| ANN 搜尋探索 | 速度與近似召回 | exact baseline 與 filter |
| candidate_k | 候選覆蓋與成本 | recall 與重排負擔 |
| RRF c | 排名貢獻衰減 | 列表來源、去重與融合權重 |
| MMR lambda | 相關性與多樣性 | 相似度尺度與證據覆蓋 |
| context budget | 證據與生成成本 | 全部包裝、tokenizer |
| score threshold | 保留或拒絕候選 | 校準資料與拒答誤差 |
| max attempts | 多步檢索成本 | 新增證據與停止條件 |

參數名稱依工具不同，這張表整理的是責任，不是宣稱各產品欄位相同。`k`、`max_results` 和 `max_tokens` 沒有可直接互換的單位。

## 名詞速查

Corpus 是資料集合；ingestion 是取得到可檢索的匯入流程；chunk 是索引片段；embedding 是向量表示；retriever 找候選；reranker 精排；grounding 是讓回答連結外部依據；provenance 是來源與轉換過程；qrels 是相關性標註；faithfulness 關心答案是否受提供的證據支持。

Agentic RAG 表示有動態檢索決策的流程；GraphRAG、RAPTOR、Self-RAG 是需分別理解的研究方向，不能只靠名稱互換。LangGraph 管理執行圖，不自動提供知識圖譜或高品質檢索。

## 公式回查

切塊數量與邊界看第 8 章；BM25 看第 11 章；cosine 與 L2 看第 12 章；RRF 看第 16 章；MMR 看第 18 章；context 預算看第 21 章；檢索指標看第 30 章；生成主張支持看第 31 章；成本看第 36 章。

公式由本機 KaTeX 排版，可離線閱讀。公式說明的是選定定義，工具實作可能用不同 IDF、gain 或空集合處理，導入前對照定義與測試。

## 原始研究路線

- [RAG：Lewis 等人](https://arxiv.org/abs/2005.11401)：參數模型與外部檢索的結合。
- [HNSW](https://arxiv.org/abs/1603.09320)：近似最近鄰索引。
- [RRF](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf)、[MMR](https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf)：融合與多樣性。
- [HyDE](https://arxiv.org/abs/2212.10496)、[Self-RAG](https://arxiv.org/abs/2310.11511)：改寫表示與反思檢索。
- [GraphRAG](https://arxiv.org/abs/2404.16130)、[RAPTOR](https://arxiv.org/abs/2401.18059)：圖與階層摘要。
- [Ragas](https://arxiv.org/abs/2309.15217)、[BEIR](https://arxiv.org/abs/2104.08663)：評估思路與資料集。

## 工程文件路線

- [Sentence Transformers](https://sbert.net/)：encoder、語意檢索與重排。
- [pgvector](https://github.com/pgvector/pgvector)、[Qdrant filtering](https://qdrant.tech/documentation/search/filtering/)：距離、索引與篩選。
- [OpenAI Embeddings](https://developers.openai.com/api/docs/guides/embeddings)、[File Search](https://developers.openai.com/api/docs/guides/tools-file-search)：自建與託管入口。
- [Gemini Embeddings](https://ai.google.dev/gemini-api/docs/embeddings)、[File Search](https://ai.google.dev/gemini-api/docs/file-search)：模型與工具支援分開確認。
- [Anthropic Contextual Retrieval](https://www.anthropic.com/research/contextual-retrieval)：片段上下文的研究設計。
- [OWASP Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)：外部文字與能力邊界。

## 版本與驗證範圍

教材整理日期為 2026-10-30。Python 基準為 3.11+；離線範例與模擬 API 測試不需要帳戶。供應商模型、價格、工具支援與配額可能變動，實際啟用時請重新確認官方文件與帳戶。付費 live 範例提供接法，未在本次建置中執行。

想繼續延伸時，先選一個你自己的小型知識領域，建立來源與十到二十個經審核問題，再逐步替換元件。每一步保留基線、失敗案例與可重跑驗收，讓知識庫與理解一起成長。
