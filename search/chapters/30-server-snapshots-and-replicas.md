# Qdrant Server：Payload Index、複本與 Snapshot 的邊界

從 Local 走向服務前，先列出需要在真實部署驗證的行為。

## 將 Local 與 Server 設定分開

正式 server 有 segments、HNSW、payload indexes、optimizers、WAL、shards 與 replicas；這些不能由 Local 的耗時或檔案格式推論。連線服務時改用受控 URL、API key、TLS 與 timeout，先確認 collection contract，再讀取健康狀態與計數。

## 一致性要以操作判讀

Write ordering、寫入等待與 read consistency 是不同設定，影響的故障與可見性條件不同。Replica 數增加不會自動讓所有讀取永遠看見最新狀態；故障切換、網路分區與過半可用條件必須依部署方案測試。將來源權威與短期同步延遲保留在服務契約裡。

## Snapshot 不是任意複製活躍目錄

使用官方 snapshot/recovery 流程，記錄 collection、設定、版本、水位與檢查碼，再在隔離目標恢復並查詢。叢集備份需要釐清 shard 與節點配置，不能只下載某一節點一份檔就宣稱完整。來源資料與事件也要有自己的備份與保留策略。

## Local 範例驗證範圍

入口只驗證 client close 後重新開啟能找到相同資料；不呼叫 server snapshot API，不建立 replica，也不驗證遠端故障切換。課程後段的災難復原專題採來源備份→全新索引重建，是另一種恢復策略，不能混稱為 server snapshot 還原。

## 部署前的實際演練

準備高/低 selectivity 查詢，建立需要的 payload indexes，記錄效果；寫入一個新版本後測各 consistency 行為；停止一個受控測試節點，測恢復與資料對帳。每項結果需附版本、拓撲與工作負載，避免把單節點成功推廣到分散式承諾。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 19_qdrant_persistence.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:19_qdrant_persistence.py -->

## 練習與解答

**請先嘗試：** Local 資料目錄重開通過，是否能將報告寫成已測 Qdrant 高可用？

<details><summary>展開解答與判斷依據</summary>

不能。只能說本機持久化通過。高可用需要真實 server 多節點、副本設定、節點故障與恢復驗收；snapshot 也要走官方服務流程並實際還原。

</details>

## 官方文件與延伸閱讀

- [Qdrant Snapshots](https://qdrant.tech/documentation/operations/snapshots/)
- [Qdrant Indexing](https://qdrant.tech/documentation/manage-data/indexing/)
- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
