# 分片、租戶與快取：速度不能打破資料邊界

規劃資料分布與查詢快取，將主體、版本與失效條件納入設計。

## Shard 不是越多越好

分片可平行處理與分散容量，也會增加記憶體、檔案、協調與小 shard 成本。租戶大小與查詢頻率不均可能形成 hot shard；只用 tenant hash 也不保證均勻。先量測每 shard bytes、QPS、更新率與尾延遲，再決定數量、routing 或大型租戶隔離策略。

## 過度切分的代價

每個小租戶一個 index/collection/partition，可能讓管理物件與資源開銷爆增。共享集合加 Filter 較省管理成本，但需要嚴格資格與 selectivity 實測。大型客戶也可能有獨立資源與備份要求。選擇依產品與工作負載，不是單一「共享」或「獨立」口號。

## Cache Key 的必要欄位

```text
principal_scope_hash + tenant + query_normalization
+ filters + generation + recipe + ranking_version + k
```

只用 query 當 key，可能將 alpha 的結果交給 beta。若權限、active 或 generation 變更，需使快取失效或在回傳前重新驗證來源。快取即使只保存 ID，也可能洩漏存在性或返回失效文件，不能免除 ACL 檢查。

## 負快取與更新

零命中可以暫存以減輕負載，但新文件寫入後可能仍看不到。設定有界 TTL、依 generation 失效與可觀察 hit/miss；記錄 cache mode，避免把舊快取結果拿來判斷新索引品質。若先前錯誤決策被反覆重現，先停用相關快取確認，再修正產生結果的流程。

## 驗收與監控

同一 query 在兩租戶、不同 role、不同 generation 下應各自隔離。變更文件為 inactive 後，快取不能繼續顯示；切換 recipe 後不得混用向量結果。監控 hot keys、每租戶資源、回源失效比例與快取導致的延遲收益，確認最佳化有實際價值。

## 練習與解答

**請先嘗試：** 快取只存 doc_id，不存本文，就可以省略 tenant 嗎？

<details><summary>展開解答與判斷依據</summary>

不行，doc_id 在不同租戶可能相同，ID 本身也可能洩漏存在性。key 與取回流程都需包含可信主體範圍，且來源 hydration 應再次驗證租戶、版本與有效狀態。

</details>

## 官方文件與延伸閱讀

- [Elasticsearch 官方參考](https://www.elastic.co/docs/reference/elasticsearch)
- [Qdrant Filtering](https://qdrant.tech/documentation/search/filtering/)
- [PostgreSQL Row Security](https://www.postgresql.org/docs/18/ddl-rowsecurity.html)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
