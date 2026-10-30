## Encoder 也可能需要指令

某些模型訓練時為 query 和 passage 使用特定前綴，或要求完整任務說明。這些字串不是任意裝飾，而是輸入分布的一部分。把它省略、翻譯或重複加入，都可能影響表示。

例如 multilingual E5 模型卡要求 query/passsage 對應前綴，連非英文輸入也要遵守。[E5 模型卡](https://huggingface.co/intfloat/multilingual-e5-small) 這是該模型的契約，不能推論所有 encoder 都需同樣文字。

## 三種常見介面

| 形式 | 設定位置 | 需要記錄 |
| --- | --- | --- |
| 文字前綴 | 實際輸入字串 | 精確前綴、空白與語言 |
| Task enum | API 參數 | query/document 等任務值 |
| 模型預設 prompt | 模型組態 | prompt 名稱、revision、覆寫值 |

不要同時由程式加一次 prefix、模型預設又加一次，形成重複指令。把最終送進 tokenizer 或 API 的輸入保存為受控診斷資料，能更快定位差異。

## 非對稱不是不相容

問題通常短、文件長；訓練可能讓不同 recipe 的表示仍落在可比較空間。需要遵守同一套配對契約，而不是強迫兩邊字串完全相同。相容性是訓練與版本定義的，不是只用「同模型」三個字概括。

若模型只提供通用 encode，不代表不能檢索；但要依模型卡手動準備相應輸入。若提供 encode_query/encode_document，也應確認預設 prompts 是否真的包含你需要的 recipe。

## 分類與聚類的設定

同一模型可能建議不同任務設定；把檢索 query recipe 直接套分類不一定最佳。API 的 task enum 也不代表所有模型版本都支援相同任務與模態。使用前查官方定義，以小題集驗證。[Gemini Embeddings API](https://ai.google.dev/api/embeddings)

## Cache 與版本

同一文字使用 query 和 document recipe，向量可能不同，所以 cache key 必須包含角色與設定。不能只以文字雜湊共用結果，也不能改 prompt 後繼續讀舊向量。

教材 `EmbeddingSpec` 分別保存 query_recipe、document_recipe，再產生設定指紋。修改其中一個 recipe 是一個可追蹤的版本變化，部署前應重新評估兩側是否需重算。

## 練習與參考答案

**題目：**換成 encode_query 後，結果沒有變，是否代表前綴完全無用？

**參考答案：**可能該模型沒有預設 query prompt，也可能文字剛好對差異不敏感。先檢查實際輸入和模型組態，再用代表性題集比較。函式名稱本身不能證明輸入已正確轉換。
