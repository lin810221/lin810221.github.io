# ANN 調參實驗：固定資料，分開品質、延遲與容量

設計能重跑的參數比較，避免把一次最快結果當成結論。

## 固定比較條件

先固定來源快照、向量 recipe、metric、查詢集合、Filter 與 Exact 真值。分開建置時間、常駐記憶體、索引檔大小和查詢耗時。HNSW 的 M、efConstruction 需要重建；efSearch 可在查詢實驗中調整。IVF-PQ 同時有訓練、桶數、碼本與 nprobe，不應一次改完所有參數。

```text
每組設定：建置 → 驗證 d / count / metric → 暖機 → 重複查詢
紀錄：recall@k、p50/p95、build_seconds、index_bytes、threads、seed
輸出：原始逐查詢結果 + 設定 manifest + 摘要
```

## 把不同誤差拆開

Exact 鄰近真值與人工相關性 qrels 是不同參考。ANN Recall 下降反映近似索引漏掉既定距離下的鄰居；nDCG 下降可能來自表示、文字分支、融合或候選漏召回。若只有最終指標，容易用增加 efSearch 去補 tokenizer 問題，花更多資源卻沒有改善。

## 看切片與尾端

分別看大/小租戶、常見/罕見 query、不同 Filter selectivity、短詞與長問題。平均延遲低不代表 p95 達標，單一極慢查詢也可能來自冷快取、GC 或 I/O。小樣本的百分位不穩定，應保存逐筆資料與重複回合，避免對細小差距下過度結論。

## 選擇可接受的工作點

畫出 Recall-延遲-容量的取捨，先設定最低品質與 p95 預算，再選成本可負擔的組合。最後在真實服務重跑包含序列化、網路、Filter、payload 與併發的測試。本課入口的 Faiss timing 只涵蓋本機 index.search；Qdrant Local 不能替 server HNSW 提供可外推的排名。

## 練習與解答

**請先嘗試：** HNSW 比 Flat 慢一次，是否代表應放棄 ANN？

<details><summary>展開解答與判斷依據</summary>

不能由一次小樣本下結論。小 N 時 Flat 高效且沒有圖遍歷開銷；增加 N、查詢批次與不同硬體後取捨可能改變。選型應依實際工作負載與重複量測，不從演算法名稱推斷必然較快。

</details>

## 官方文件與延伸閱讀

- [Faiss Indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)
- [Qdrant Indexing](https://qdrant.tech/documentation/manage-data/indexing/)
- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
