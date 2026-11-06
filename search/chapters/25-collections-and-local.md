# Qdrant Collection 與 Local：先建立正確的向量空間

實際建立 named dense 與 sparse vectors，分清本機 SDK 與遠端服務的責任。

## Collection 的契約

Collection 定義向量名稱、維度、distance 及相關設定。每個 point 有 ID、vector 與 payload。本課 dense 為八維 cosine，lexical 為固定詞彙表的 sparse vector；兩者屬於同一 point，可以在 Query API 中分別召回。既有 collection 啟動時需檢查設定，不能只因名字存在就假定可用。

## Local 模式是真的查詢，但不是遠端叢集

`QdrantClient(location=":memory:")` 在程序內執行；`path=...` 可保存本機資料。它方便驗證 points、payload filters、Query API 與持久化。它不經過服務網路，也不能代替 Qdrant server 的 HNSW、payload index、replication、snapshot 與高併發效能驗證。

## ID 與 Payload 的用途

本課 point ID 穩定對應來源文件；payload 只保存 tenant、doc_id、revision、active、recipe。本文仍從來源取回，避免另一份內容快取變舊。真實系統可保存展示欄位，但要明確定義版本與權威來源，不讓搜尋返回的舊 payload 覆蓋新資料。

## 第一個可重現流程

開啟 client、建立或驗證 collection、upsert、query_points、讀取 ID 與 payload、close。入口使用 context manager 確保關閉。替換成遠端 client 時，仍需提供受控 URL、TLS、認證、timeouts 與部署驗收；並確認 server 與 SDK 相容，不能把 Local 成功直接當遠端已完成。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 15_qdrant_local.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:15_qdrant_local.py -->

## 練習與解答

**請先嘗試：** 把 Local 的 path 指到共享網路磁碟，是否就能讓多程序當資料庫使用？

<details><summary>展開解答與判斷依據</summary>

不應如此推論。Local 有其檔案鎖與使用限制，不是多程序遠端服務。需要共享存取、併發與高可用時啟動正式 Qdrant server，使用官方連線與服務級驗收。

</details>

## 官方文件與延伸閱讀

- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)
- [Qdrant Indexing](https://qdrant.tech/documentation/manage-data/indexing/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
