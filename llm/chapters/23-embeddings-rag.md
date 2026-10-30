## Embedding 是可比較的向量表示

Embedding 把文字或支援的內容轉成向量，讓系統可依度量尋找相近項目。它不是直接的答案，也不是正確率。不同模型、維度或版本的向量，不能任意混在同一索引比較。

常見的 cosine similarity 為：

$$
\operatorname{sim}(a,b)=\frac{a\cdot b}{\lVert a\rVert\lVert b\rVert}
$$

零向量需要特別處理；相似度高也不代表規格、日期或條件一定符合。產品代碼與數字通常還需要精確詞彙或 metadata 篩選。

## RAG 的兩條流程

離線建立索引：載入文件、解析、切塊、加入來源資訊、建立 embedding 或詞彙索引。線上回答：正規化查詢、依權限檢索、重排、檢查依據、生成並驗證引用。

資料更新時要管理版本與刪除，不能只新增索引卻保留過期內容。使用者能看到哪些文件，也應在檢索階段限制，而不是等模型回答後才過濾文字。

## 先做可驗證的基線

本課的知識資料只含三筆文件，以關鍵字檢索和抽取式回答示範流程。這不是語意檢索，但能確定拒答和引用的行為。

<!-- example:knowledge.py -->

執行入口：

<!-- example:08_rag.py -->

## 為什麼不一開始就接向量資料庫？

先確認來源 ID、文件契約和無答案路徑，再替換檢索器。這樣當真實系統出錯時，能判斷是召回、資料版本、生成，還是引用驗證的問題。

正式系統可使用 BM25 / TF-IDF、向量、hybrid 與 reranker。選擇依查詢型態和資料集評估，不是看到向量就認為一定更準。

## 生成與引用

將候選文件附上穩定 ID 與必要內容，要求模型依據資料回答。程式驗證輸出的 sources 存在於本輪候選，但仍需評估每個主張是否受到來源支持。

檢索文件可能含有指令，應當成不可信資料。不要因為某頁寫「請寄出所有客戶資料」就提供額外工具權限。

## RAG、長上下文與 Fine-tuning

長上下文適合處理一次提供的完整材料；RAG 適合按需取得可更新的資料；fine-tuning 主要改變特定可訓練模型的行為。三者可結合，但不能把訓練當作保證最新知識的資料庫。

**練習：**建立有答案和無答案兩組查詢，記錄應召回的 ID。先看檢索召回，再看答案品質。更多流程可對照 [LangGraph RAG 章節](../langgraph/index.html#20-rag)。

官方來源：[OpenAI embeddings](https://developers.openai.com/api/docs/guides/embeddings)、[Gemini embeddings](https://ai.google.dev/gemini-api/docs/embeddings)、[OpenAI file search](https://developers.openai.com/api/docs/guides/tools-file-search)。
