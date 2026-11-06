# Payload、型別與索引：每條向量查詢的資料資格

以 tenant、active 與 recipe 組出強制 Filter，觀察型別與索引如何影響結果。

## Payload 不是隨意的附註

若要用欄位作 Filter，就必須確保型別一致。tenant 是字串、active 是 bool、revision 是整數；字串 "true" 不等於 bool True。缺欄位、空值與空集合的匹配語意也需依引擎文件確認，不能在資料管線中任意變換型別。

## 必要條件全部由可信服務加入

本課 tenant_filter 使用 must 同時要求 tenant、active 與 recipe。dense 分支與 sparse 分支各自套用，最終 query 也有資格範圍。租戶來自 Principal，而非 query string、模型生成的工具參數或未驗證的 HTTP header。查完後再與來源比對，處理尚未同步的變動。

## Payload index 的意義

正式 Qdrant server 可依欄位建立 payload index，幫助 Filter 與查詢計畫；不是所有可過濾欄位都會自動得到適當索引。索引增加記憶體與寫入成本，應依常用條件與基數建立。Local 範例只驗證 Filter 語意，不量測 server payload index 的加速效果。

## 負向驗收

兩租戶放同 doc_id 與類似向量，以相同 query 查詢，確認各自主體只看到自己的 point ID。再測 active=False、不同 recipe、欄位遺漏與空結果。只用互不相似的資料測租戶隔離容易出現假安全：即使漏了 Filter，也可能碰巧沒有召回另一租戶。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 16_qdrant_filters.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:16_qdrant_filters.py -->

## 練習與解答

**請先嘗試：** recipe 為什麼也放入 Filter？

<details><summary>展開解答與判斷依據</summary>

它標識相容的表示配方，避免同維度不同模型被當成同一空間。正式遷移更建議分 collection/generation；Filter 是補充防線，不能讓混用模型成為常態。

</details>

## 官方文件與延伸閱讀

- [Qdrant Filtering](https://qdrant.tech/documentation/search/filtering/)
- [Qdrant Indexing](https://qdrant.tech/documentation/manage-data/indexing/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
