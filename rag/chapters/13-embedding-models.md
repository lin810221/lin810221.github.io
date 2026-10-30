## 選擇模型時看什麼

先看自己的語言、領域和檢索任務。一般英文句子相似度表現，不等於繁體中文法規、產品型號或混合中英文件的檢索效果。準備同義改寫、精確代碼、長段落和無答案題，測量模型是否真的能找到需要的證據。

同時比較最大輸入、維度、延遲、批次能力、可用部署方式與成本。這些是不同軸線，維度高不保證品質高，模型大也不保證你能接受其記憶體與延遲。

## 文件與問題必須使用相容設定

保存 `provider`、`model`、`revision`、`dimensions`、`normalization`、`task_type` 與前處理版本。部分模型對 query 和 document 使用不同前綴或任務設定，應照該模型文件處理，不能自行把所有文字加上同一個 instruction。

OpenAI Embeddings 的請求包含 `model` 與 `input`，回應 `data` 帶索引與向量；`text-embedding-3-small` 可作明確示範名稱。以下程式預設只展示請求，使用 `--live` 才送出。模型可用性與限制請以帳戶及官方文件為準。[OpenAI Embeddings](https://developers.openai.com/api/docs/guides/embeddings)

<!-- example:13_openai_embeddings.py -->

## 讀懂共用 adapter

`provider_http.embeddings()` 明確要求 float 表示，按回傳的 `index` 排序，確認索引正好對應全部輸入，再檢查維度和有限數值。不能只依網路回傳列順序，把第一個向量塞給第一個片段。錯配後，向量搜尋看似正常卻會接上錯誤來源。

範例不會列印 API Key，也不會自動重試。大量文件正式匯入需要批次切分、速率限制、有限退避與冪等記錄。教材為了透明只送出兩個短句，避免一開始就把大量私人文件交給服務。

## 其他可選路線

Gemini API 提供 Embedding 模型與不同任務設定，具體名稱、模態與適用限制需查當前文件。[Gemini Embeddings](https://ai.google.dev/gemini-api/docs/embeddings) 也可以選擇本機 Sentence Transformers 模型，在受控環境先下載模型權重，再以固定版本執行；首次下載需要網路和磁碟空間。[Sentence Transformers](https://sbert.net/)

生成器與 Embedding 不必同一家。例如用一個適合中文的本機 encoder 檢索，再把已授權證據交給 Claude 生成。相容性要求在同一個向量空間的 query/document 之間，不要求生成器也使用同樣供應商。

## 模型遷移怎麼做

新建另一個索引，重算全部文件向量，使用固定評估集比較召回與延遲，通過後切換。舊索引保留回復窗口。切換時一起更新查詢 encoder、快取版本與監控標籤，避免新舊表示混用。

## 練習與參考答案

**題目：**為了節省空間，把一個 1536 維向量直接截成前 256 維可行嗎？

**參考答案：**只有模型明確支持降維或特定表示方式時，才能依其文件與評估使用。一般向量任意截斷可能破壞資訊。應使用模型支援的參數或已驗證的降維方法，並重建查詢與文件兩側設定。
