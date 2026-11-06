# 向量 Filter 與候選預算：先過濾還是後過濾

用固定排名模擬候選耗盡，再辨識真正資料庫執行計畫的不同做法。

## Top-k 的集合不能含糊

想找 alpha 的五篇文件，真值是 alpha 集合內最接近的五篇。若先取全域五篇、再刪掉 beta，可能只剩一篇；這不是正確的 scoped top-5。提高候選數可降低不足機會，卻不能用固定倍數保證任意 selectivity 下都足夠。

## Pre-filter 與 Post-filter 的權衡

先界定可查集合可以維持資格，但 ANN 圖遍歷如何與 Filter 結合取決於引擎。可能使用 payload index、圖上條件、切換 exact scan 或迭代擴大掃描。Post-filter 較容易套在外層，卻可能耗盡候選。兩者都需要真實資料分布與查詢條件量測。

## 安全檢查與品質檢查分工

每路 Filter 保護召回集合；來源 hydration 再保護最新租戶、版本與 active。最後檢查能拒絕無權文件，但救不回因全域候選預算太小而沒召回的有效文件。因此測試要同時檢查沒有越權，以及在允許集合內的 Recall，而不只是結果全都符合條件。

## 瀏覽器與 Python 實驗邊界

本例用固定的全域排序與 allowed ID 集合，對照 post-filter 預算和 eligible-first 真值。它清楚說明候選不足機制，沒有實作 HNSW，也沒有量測某個服務的優化器。正式服務還需要記錄候選數、Filter selectivity、索引使用情況與 p95，再決定預算或 exact fallback。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 14_filter_candidates.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:14_filter_candidates.py -->

## 練習與解答

**請先嘗試：** 回傳的每篇都屬於 alpha，是否就能證明 Filter 搜尋正確？

<details><summary>展開解答與判斷依據</summary>

只能證明這些結果沒有跨租戶，不能證明召回足夠。需與 alpha 可查集合內 Exact 真值比較，並驗證在低 selectivity、active 變更與 recipe 不同時的候選不足行為。

</details>

## 官方文件與延伸閱讀

- [Qdrant Filtering](https://qdrant.tech/documentation/search/filtering/)
- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
