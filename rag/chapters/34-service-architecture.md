## 從單一程式到服務

離線 CLI 讓你理解演算法；多人服務還需要身分驗證、請求限制、併發、監控與資料持久化。先列出需要的元件，而不是直接把所有程式塞進一個 HTTP endpoint。

典型元件包含前端、查詢 API、背景匯入 worker、文件儲存、metadata 資料庫、全文或向量索引，以及模型 adapter。它們可以先在同一台機器不同模組運作，需求成長後再分離部署。

## API 契約範例

```json
{
  "request_id": "req-123",
  "status": "answered",
  "answer": "須提前三個工作日。[S1]",
  "citations": [{"label":"S1", "doc_id":"leave", "version":"2026-10", "page":2}],
  "corpus_version": "2026-10-a"
}
```

使用者提交 question、conversation ID 等允許欄位；tenant、角色與索引範圍由可信伺服器決定。不要把來自瀏覽器的 `roles=[admin]` 直接轉成查詢權限。

## 匯入工作使用狀態機

```text
received → parsing → chunking → embedding → indexing → validating → ready
                    ↘ failed / retryable / rejected
```

每個工作保存來源版本、處理版本與進度，對應可重試的批次。前端顯示的是已驗證狀態，不能在 received 階段就標示知識庫可用。失敗文件應有可理解原因，方便補檔或重試。

## 併發與資源

同步 HTTP endpoint 不應長時間進行大型 PDF OCR。匯入走背景工作；查詢有 timeout 與併發限制。模型 API 限流時要有有界重試與錯誤分類，不讓所有使用者請求同時重試形成尖峰。

資料庫連線、向量索引和本機模型各有執行緒與程序限制。不要把單一記憶體字典當作多程序共用資料庫；不同 worker 可能各有一份副本。需要共同狀態時使用明確儲存與交易。

## 完整性與服務可用性

索引更新採新版本建置再切換，查詢期間固定讀同一版本。若需要回復，把讀取指標切回前一完整版本，並同步快取版本。文件來源故障不一定影響已建立的可用索引，兩種健康狀態應分開顯示。

對使用者回傳合適的狀態：無證據、需澄清、生成 timeout、索引尚未 ready、未授權。內部 trace 保存錯誤原因，外部不暴露金鑰與私人文件內容。

## 練習與參考答案

**題目：**API 收到上傳檔後立即回「匯入成功」，背景解析十分鐘後失敗，使用者應看到什麼？

**參考答案：**最初應回工作已接收及 job ID，之後提供 parsing、failed 或 ready 狀態。只有全部索引與驗證完成才顯示可檢索。若失敗，明確指出尚未更新知識庫，保留舊版服務。

延伸閱讀：[FastAPI background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
