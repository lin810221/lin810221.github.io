# HNSW：圖結構、建置成本與搜尋廣度

執行真正 Faiss HNSW，量測近似召回，分清 M、efConstruction 與 efSearch。

## 圖上的近鄰搜尋

HNSW 以多層鄰近圖協助從入口逐步接近查詢。高層提供長距離移動，底層保留更多候選。它是近似演算法，不保證每次找到全域最近鄰；效果依資料分布、建置順序、參數與實作而異。常見平均效率敘述不等於所有輸入的最壞時間保證。

## 三個參數分別花在哪裡

M 影響圖連線數、記憶體與建置；efConstruction 影響插入時搜尋候選廣度與圖品質；efSearch 影響查詢時探索。提高 efSearch 常能改善 Recall，同時增加計算，但不保證每個工作負載嚴格單調。想改 M 通常要重建，不能把所有參數當查詢端即時旋鈕。

## 實際跑一次對照

入口建立 2048×32 的固定 normalized 資料，先跑 Flat 真值，再跑 HNSW，計算 Recall@k 與暖機後搜尋耗時。固定一個執行緒只是減少教學量測變動；結果不是生產流量、沒有網路與 payload 讀取，也不是跨產品速度排名。

## Filter 與刪除取決於實作

不同系統將 Filter、刪除標記、圖維護與重建整合的方式不同。Faiss 的 HNSW 能力不能直接套成 Qdrant 或 Elasticsearch 的 API；Qdrant Local 也不是 server HNSW 的效能替身。選擇資料庫時應測試真實 Filter selectivity、更新率與刪除後行為，而非只看無 Filter 圖搜尋。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 12_faiss_hnsw.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:12_faiss_hnsw.py -->

## 練習與解答

**請先嘗試：** efSearch 已拉高仍漏掉某類查詢，還能檢查什麼？

<details><summary>展開解答與判斷依據</summary>

先確保 Exact 真值與 Filter/metric 一致，再檢查圖建置品質、M、efConstruction、資料分布與表示模型。若 Exact 本來就無關，調 ANN 參數無法修復語意品質。

</details>

## 官方文件與延伸閱讀

- [Faiss Indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)
- [Qdrant Indexing](https://qdrant.tech/documentation/manage-data/indexing/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
