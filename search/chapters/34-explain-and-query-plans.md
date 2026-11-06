# EXPLAIN：確認資料庫實際做了什麼

讀懂掃描、排序、估計值與實際值，區分 SQL 正確和查詢計畫有效率。

## 先看計畫，再看毫秒

EXPLAIN 顯示 planner 的選擇；EXPLAIN ANALYZE 會真正執行查詢，輸出實際資料與時間，對變更語句尤其要注意效果。本課服務實驗只建議對受控的唯讀 SELECT 使用 ANALYZE、BUFFERS，避免在未知生產表上隨意執行高成本查詢。

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT doc_id FROM search_documents
WHERE tenant = 'alpha' AND active
ORDER BY embedding <=> '[1,0,0,0,0,0,0,0]'::vector LIMIT 5;
```

## 讀取關鍵欄位

檢查 Index Scan 或 Sequential Scan、Filter、Rows Removed by Filter、Sort、loops、估計 rows 與實際 rows。Estimated cost 不是毫秒；多層節點時間與 loops 也不能簡單全部相加。BUFFERS 區分記憶體命中與讀取，但快取可能不等於實體磁碟完全沒有 I/O。

## 小表走 Seq Scan 不一定錯

幾百筆資料掃全表可能更便宜，尤其 Filter 很窄或索引啟動成本較高。統計過期、分布偏斜或不同 tenant 的大小，也會影響估計。不要先把 enable_seqscan 關掉再宣稱索引更快；這類設定只適合作診斷對照，正式決策要回到正常 planner。

## 用計畫解釋品質

ANN 計畫的 Filter 行為可能讓回傳不足 k，而 exact plan 可找到更多。需將執行計畫與品質真值一起保存。若加入次要排序或包裝距離表達式導致索引失效，先決定是否需要外層重排，不用不透明 SQL 技巧換取看似穩定名次卻漏掉索引。

## 形成可重現證據

報告附 server/extension 版本、索引 DDL、資料筆數、Filter selectivity、設定與原始 EXPLAIN。用相同查詢在暖/冷與不同併發條件重複測量。只貼一張最快截圖，無法區分索引改善、快取命中或偶然的背景負載差異。

## 練習與解答

**請先嘗試：** 計畫估計 100 筆，實際只有 1 筆，應直接調 ef_search 嗎？

<details><summary>展開解答與判斷依據</summary>

先判斷估計偏差的來源，包含統計、相關欄位與租戶分布；再分開檢查 ANN 掃描不足。ef_search 是查詢探索預算，不能代替 planner 統計與正確 Filter 設計。

</details>

## 官方文件與延伸閱讀

- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html)
- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
