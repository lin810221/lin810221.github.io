# pgvector HNSW、IVFFlat 與 Iterative Scan

理解索引建置、查詢參數與 Filter 後候選不足，再用真實計畫驗證。

## HNSW 與 IVFFlat 的建置差異

HNSW 以圖作近似查詢，有建置時間與記憶體成本；IVFFlat 需要代表性的資料分桶，lists 與 probes 影響候選範圍。pgvector 的 IVFFlat 與 Faiss IVF-PQ 不同：前者不能因名字有 IVF 就假定已使用 PQ 壓縮。索引、度量與型別支援應依 0.8.7 官方文件確認。

## Filter 與索引掃描

近似索引掃描後套 WHERE，可能剩下不足 k 的資料。低 selectivity 租戶特別容易出現這個問題。提高 hnsw.ef_search 或 ivfflat.probes 可增加工作量；iterative scans 可在特定條件下繼續搜尋，但仍受掃描與記憶體上限控制，不是無限制的 exact 保證。

```sql
BEGIN;
SET LOCAL hnsw.ef_search = 100;
SET LOCAL hnsw.iterative_scan = strict_order;
-- 在同一交易執行有 tenant / active 的向量查詢
ROLLBACK;
```

這是受控服務實驗配方，不由離線範例自動執行。strict/relaxed ordering 的保證與可能重排需求應分開確認，切勿以事後排序掩蓋候選本來沒被掃到。

## 其他可選策略

資料很小或 Filter 很窄時，B-tree 過濾後 exact scan 可能更合適。少量固定類別可評估 partial index；大量大租戶可評估 partition。索引數太多會增加寫入與維護成本，避免一個小租戶就建一個專用索引。先用工作負載與執行計畫判斷。

## 比較標準

同一租戶資格內建立 Exact 真值，量測每種 Filter selectivity 的 Recall、返回數與 p95。保存 EXPLAIN、索引定義、資料量、work_mem 與相關設定。這些服務端行為未由本課 Local/Faiss 測試覆蓋，需在你啟動的 PostgreSQL 實驗環境確認。

## 練習與解答

**請先嘗試：** 查詢有 LIMIT 10 卻只有三筆，是不是資料只剩三筆？

<details><summary>展開解答與判斷依據</summary>

可能是資格集合本就不足，也可能是 ANN 候選在 Filter 後耗盡。先用相同條件 exact count/真值確認，再觀察索引計畫、掃描預算與 iterative scan，不能直接推論來源缺資料。

</details>

## 官方文件與延伸閱讀

- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
