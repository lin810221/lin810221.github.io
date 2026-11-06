# PostgreSQL Schema 與全文索引：讓搜尋靠近關聯資料

用 typed schema、tsvector 與 GIN 組織搜尋資料，同時保留業務交易。

## 何時考慮單一關聯資料庫

資料本來就在 PostgreSQL，且需要交易、join、精確條件與向量查詢時，pgvector 可減少一套外部同步流程。但全文分析、分散搜尋與專用向量服務的能力仍需比較；不是把所有資料放同一庫就沒有資源隔離與查詢計畫問題。

## Schema 的構成

本課 SQL 建立 vector extension、來源欄位、vector(8)、generated tsvector、GIN 與向量 HNSW 索引。`simple` text search configuration 是可重現的教學基線，不代表中文斷詞方案。title/body 可用 setweight 設定 A/B 權重，再以 tsquery 與 rank 函數查詢。

## 交易與派生表示

若來源與已計算向量在同一筆 PostgreSQL transaction 寫入，可以獲得該交易的原子性。但外部 embedding 計算仍可能失敗或很慢；不要在長交易內等待模型網路回應。可先保存待處理狀態，再以受控 worker 寫入向量與 recipe，讀取時明確篩選已完成資料。

## 範例的安全執行範圍

入口只輸出 data/pg_schema.sql，不自動連線、不執行 CREATE EXTENSION，也不替你變更資料庫。要在獨立測試庫使用，先確認 PostgreSQL 18.6、extension 0.8.7 已安裝與角色權限，再由你執行 SQL。DDL、RLS 與索引計畫需在真實服務另外驗證。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 20_pg_schema.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:20_pg_schema.py -->

## 練習與解答

**請先嘗試：** 有 GIN 與 HNSW 索引，查詢時是否一定兩個都使用？

<details><summary>展開解答與判斷依據</summary>

不一定，planner 依查詢、統計與成本選擇計畫。全文與向量可能先分支取候選再融合，或先精確過濾；使用 EXPLAIN 驗證，不能從 schema 裡有索引就推論實際已走索引。

</details>

## 官方文件與延伸閱讀

- [PostgreSQL 全文搜尋](https://www.postgresql.org/docs/18/textsearch.html)
- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)
- [PostgreSQL 18 官方文件](https://www.postgresql.org/docs/18/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
