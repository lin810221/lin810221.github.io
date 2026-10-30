## 什麼變更需要重新評估

模型、revision、pooling、前綴、維度、正規化、量化與 parser 都可能改變表示。文件內容更新又是另一種資料變更。把它們分開記錄，再決定哪些向量需重算和哪些門檻需重新校準。

只改 query encoder 而保留舊文件，常造成同維度不相容。系統不一定報錯，卻可能從此找出毫無依據的近鄰；版本契約應先攔下這種情況。

## 安全的遷移順序

```text
保存舊版可用索引
→ 新 encoder 與設定指紋
→ 重算文件並建立新索引
→ 完整性與固定題集評估
→ 影子比較／受控切換
→ 觀察品質與延遲
→ 保留回復窗口後清理
```

影子查詢讓新版本處理相同輸入但不直接影響使用者結果；成本與資料處理仍要控制。切換時同時切 query recipe、文件索引和 cache scope，不能各自更新。

## 服務介面

```json
{
  "request_id":"embed-search-123",
  "encoder_spec":"fingerprint",
  "corpus_version":"v5",
  "hits":[{"id":"doc-a","score":0.82}],
  "score_type":"cosine"
}
```

這是自訂應用回應，方便追查。score_type、設定與 corpus 都要能解讀，否則升級後同一數字可能被前端錯當機率或舊門檻。

## 回復需要對應資料

保留舊模型卻刪掉舊索引，通常不能立即回復。舊 cache 也不應跨回新空間。文件權限異動需要在兩版共同更新，避免回復時把已撤權資料重新公開。

## 相依套件與模型卡

固定套件版本、tokenizer 和模型 revision，保留最終輸入與前處理。載入框架支援 revision、local_files_only 等設定，但應用仍需把它們實際納入 manifest。[SentenceTransformer](https://sbert.net/docs/package_reference/sentence_transformer/model.html)

若模型服務無法提供永久不變版本，記錄實驗時間與可重現限制，不聲稱完全相同條件。用固定探測 query 監控可能變化，但別用單一分數猜測供應商內部原因。

## 練習與參考答案

**題目：**新模型提升了平均分，但 p95 延遲超標，能否只把一半文件換新向量？

**參考答案：**不要在同一比較空間混用不相容向量。可以保留兩套完整路由、對特定任務選模型，或優化批次與索引；每條路徑的 query/document 契約要完整。
