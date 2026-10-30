## 模型與操作要分開

Gemini Embedding 可用於相似度、檢索、分類或聚類等任務；模型與 API 支援仍需按當前文件確認。本例使用明確的文字模型 `gemini-embedding-001` 和同步 `batchEmbedContents`，不把其他模態能力推論到所有端點。

REST `requests` 內每筆包含 model、content 與設定；回應 embeddings 依官方定義保持輸入順序。這與 OpenAI 以 index 配對的解析方式不同。[Gemini Embeddings API](https://ai.google.dev/api/embeddings)

## 任務設定屬於輸入契約

查詢和文件可使用 `RETRIEVAL_QUERY`、`RETRIEVAL_DOCUMENT`；其他任務應依模型建議選擇。它們影響 encoder 的任務條件，不能把同樣文字不同角色的向量無條件放在同一快取鍵下。

本次核對的 REST schema 使用 `embedContentConfig`，內部欄位如 `taskType`、`outputDimensionality`；Python SDK 的 `EmbedContentConfig` 則使用 snake_case。文件將舊版請求頂層的相關欄位標成 deprecated，因此範例採巢狀設定。

## 執行 dry run

<!-- example:18_gemini.py -->

```powershell
python 18_gemini.py
python 18_gemini.py --task RETRIEVAL_QUERY
# 設定自己的 GEMINI_API_KEY 後才選擇 live
python 18_gemini.py --live
```

程式以 `x-goog-api-key` header 傳金鑰，不把它放在 URL 或列印輸出。預設只展示兩句教材的請求，不會連線。

## 不同的 batch

同步 batch 讓多筆輸入一起回應；非同步 batch 可能先回工作狀態，之後取輸出。兩者延遲、失敗重試和讀取方式不同，不能因名稱都叫 batch 就用相同 parser。

本例驗證回應數量、維度和數值。若長度不符，整批不直接寫入正式索引；保留輸入識別與工作狀態再處理。對 query/document 兩組向量，也要保存相同模型和相容設定。

## 降維與正規化

降維能力、允許值及輸出是否需要自行正規化，依所選模型和設定確認。不要把一個供應商對某模型的建議套到所有模型。縮短後重新評估召回和門檻，並更新 manifest。

## 練習與參考答案

**題目：**Python SDK 範例使用 `task_type`，能直接把它放進 REST JSON 頂層嗎？

**參考答案：**應依 REST schema 使用對應層次與 camelCase，不能只改語言不改介面。教材提供的 payload builder 和測試明確檢查 `embedContentConfig.taskType`，避免沿用不同版本欄位。
