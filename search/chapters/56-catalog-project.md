# 完整專題：可更新、可隔離的商品混合搜尋

把來源、FTS、Qdrant、候選融合與最新資格驗證組成一條可執行服務。

## 輸入契約

CatalogSearch 以已驗證 Principal 初始化，search 只接受 text 與有限 k。它不接受 query 裡自選 tenant。專題使用 alpha/beta 固定身分作離線示範，這不是登入系統；真實服務需在請求邊界建立主體並檢查 scope。

## 候選到結果的路徑

先從 FTS 和 Qdrant dense 取得各自受租戶限制的候選，再逐個向量 hit 回來源取文件。必須核對 tenant、doc_id、recipe、revision 與 active；不符就丟棄。最後用應用層 RRF 融合。Qdrant dense 是人工特徵，專題不預設執行模型或 reranker。

## 為什麼不直接展示 Payload

在 worker 尚未同步的窗口，向量庫可能含舊版本或已刪 point。來源檢查保護當前資格。測試也注入偽造的跨租戶候選，確認就算召回端有錯，服務也不會直接顯示。此防線不等於召回可以省略 Filter，因為錯候選仍會擠掉有效名額。

## 可以觀察的狀態

入口先查詢、再在來源 tombstone 一筆但尚未 replay，觀察過期候選被隱藏；最後 replay 後確認向量也清除。輸出 mode、discarded 與穩定 IDs。它是一個核心模組與 CLI 專題，不假裝已部署 HTTP server 或多租戶認證系統。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 31_catalog_project.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:31_catalog_project.py -->

## 練習與解答

**請先嘗試：** 來源版本更新但 worker 還沒算完新向量，舊向量指到最新來源時可以直接展示嗎？

<details><summary>展開解答與判斷依據</summary>

本課採嚴格版本一致，拒絕 stale vector 候選，避免用舊內容距離冒充新內容匹配。產品可另定弱一致策略，但要標示與評估；來源 active/tenant 等硬資格仍不可放寬。

</details>

## 官方文件與延伸閱讀

- [SQLite FTS5 官方文件](https://www.sqlite.org/fts5.html)
- [Qdrant Filtering](https://qdrant.tech/documentation/search/filtering/)
- [Elasticsearch RRF Retriever](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/retrievers/rrf-retriever)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
