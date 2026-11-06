# Segment、Refresh、WAL 與複本：四種不同的承諾

分清可搜尋、可恢復、可讀到最新與可災難復原，不用單一成功訊號概括。

## 可見性與持久性

搜尋引擎的 refresh 讓新的索引視圖可被搜尋；WAL/translog 等日誌協助故障恢復；flush/checkpoint 將狀態推進到另一個持久化階段。各產品名稱與具體語意不同，不能把 SQLite WAL、PostgreSQL WAL 與 Elasticsearch translog 當相同 API。更不能由「查得到」直接推論「已有可還原備份」。

## Segment 合併與刪除

索引常以 segments 組織資料，合併可減少讀取開銷並回收刪除資料，但需要 CPU、I/O 與額外暫存。大量小批次 refresh 或高頻更新可能增加 segment/merge 壓力。Force merge 不是一般查詢慢時的萬用修復；先確認索引狀態、寫入與官方建議使用情境。

## 複本的角色

Replica 可提高可用性與分攤讀取，但不是備份。錯誤刪除或壞資料可能很快複製到所有節點。Read-your-writes、quorum 與 replica lag 依配置和故障情況而異；應為每項服務承諾寫出可測條件，而非只寫 replicas=2 就宣稱資料永不遺失。

## 故障窗口表

| 情況 | 要問的問題 |
|---|---|
| 寫入回應成功後程序當機 | 日誌是否依設定持久化，重啟能否恢復 |
| 一個節點失效 | 讀寫能否繼續，副本與一致性如何 |
| 誤刪全索引 | 有沒有獨立備份或來源重建路線 |
| source/index 延遲 | 查詢資格是否安全，lag 是否在 SLA 內 |

## 本課的證據界線

本機測試覆蓋 FTS 交易、Local 重開與來源重建；沒有停掉真實叢集節點，也沒有測遠端 fsync、quorum 或多區恢復。這些需在正式服務的隔離環境注入故障，保存版本與設定，再將結果納入部署報告。

## 練習與解答

**請先嘗試：** Replica 都正常，是否可以取消備份？

<details><summary>展開解答與判斷依據</summary>

不行，複本通常會同步錯誤刪除和壞資料。備份需要獨立保留點與實際還原；也要明確來源重建能接受的 RPO/RTO，以及事件是否足夠追趕。

</details>

## 官方文件與延伸閱讀

- [PostgreSQL 18 官方文件](https://www.postgresql.org/docs/18/)
- [Elasticsearch 官方參考](https://www.elastic.co/docs/reference/elasticsearch)
- [Qdrant Snapshots](https://qdrant.tech/documentation/operations/snapshots/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
