# Query Points 與 Prefetch：候選、輸出與成本

讀懂新版 Query API 的查詢層次，設定有界候選而非只調最後的 limit。

## Query API 的兩個階段

prefetch 先取得一條或多條候選路徑，主 query 再進行融合、重排或其他處理。每個 prefetch 的 limit 決定候選上限，外層 limit 決定回傳數量。外層要求十筆但各路只有三筆不同候選，不會憑空補成十筆；可查集合本來不足時也應回真實數量。

```python
models.Prefetch(query=dense, using="dense", filter=boundary, limit=20)
models.FusionQuery(fusion=models.Fusion.RRF)
```

這些模型來自 qdrant-client 1.20.0。舊教學常用的不同 search 入口，不應直接照貼到新版本；先檢查當前方法簽名與官方 Query API。版本升級時保留序列化與語意測試。

## 控制回傳欄位

with_vectors=False 可避免為展示結果傳回整個向量；with_payload 可限制必要欄位。這減少傳輸與不必要資訊，但不是 ACL 替代品。若後續再用 point ID retrieve，仍需確保身份與租戶範圍，不讓 ID 查詢繞過搜尋端 Filter。

## Score 與 Threshold

distance 不同，score 方向與閾值意義也可能不同。融合分數更不等於原始 cosine；不要把 dense 的 score_threshold 原封套到 RRF。先用固定小資料檢查語意，再用評估集挑選適合門檻；結果不足時回傳少量或空集合，比混入低品質文件湊 k 更可解釋。

## 查詢成本是整條路徑

Prefetch 數、每路 budget、Filter、payload 與 rerank 共同決定耗時。單看最終 limit 無法預測成本。服務日誌應保留每路設定、候選數與完成狀態，才能在品質下降或負載升高時找出是哪個階段造成。

## 練習與解答

**請先嘗試：** 外層 limit=5，兩個 prefetch 各 limit=1000，是否只是取五筆所以很便宜？

<details><summary>展開解答與判斷依據</summary>

不是，前段仍可能執行大量候選搜尋與融合。需同時限制每路 budget、查詢時間與輸出大小，並測量真實 workload。輸出數與內部工作量是不同概念。

</details>

## 官方文件與延伸閱讀

- [Qdrant Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/)
- [Qdrant Filtering](https://qdrant.tech/documentation/search/filtering/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
