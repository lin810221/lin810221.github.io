# Faiss Flat：真正的全量向量檢索

用 float32 連續矩陣建立 IndexFlatIP，與 NumPy Exact 逐筆比較。

## Flat 沒有近似捷徑

IndexFlatIP 保存向量並對查詢計算內積；IndexFlatL2 使用平方 L2。它不需要 training，適合當真值與小型系統的基線。單次掃描成本隨 N×d 增加，批次計算、SIMD 與硬體會影響實際耗時；不要只用漸近式判斷小資料下哪個索引比較快。

## 正確傳入矩陣

Faiss 使用維度一致的 float32 連續陣列。本課先檢查 finite、shape，針對 cosine 路線將文件與查詢都 normalize，再送入 IP 索引。只 normalize 查詢不 normalize 文件，會使文件長度改變排名。搜尋多查詢時保留二維 shape，即使只有一筆也用 (1,d)。

## 內部位置與業務 ID

Flat 的預設結果是加入順序的位置，不等於業務 doc_id。可用映射表或適當 ID wrapper，刪除或重建後保持對應。查不到的填充值與超過筆數的 k 也要處理，不能拿負索引意外讀到最後一筆資料。本課入口使用有界 k 與固定位置映射。

## 比較與持久化

入口以固定 seed 產生 normalized 資料，將 Faiss 與 NumPy 真值的 ID/score 對照。序列化檔只能載入可信來源；checksum 偵測內容變動，但沒有簽章或可信來源就不能證明安全。Faiss 不是具備多租戶 ACL、交易與自動備份的完整資料庫，這些責任需在服務層補上。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 11_faiss_flat.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:11_faiss_flat.py -->

## 練習與解答

**請先嘗試：** 把 Flat 換成 HNSW 後，原本的來源 ID 映射還需要嗎？

<details><summary>展開解答與判斷依據</summary>

需要，索引只知道其位置或指定 ID。來源 hydration、刪除與版本檢查都依賴穩定對應。索引檔、ID 映射、recipe 與來源水位應成套保存，避免重建後指到錯文件。

</details>

## 官方文件與延伸閱讀

- [Faiss 官方文件](https://faiss.ai/)
- [Faiss Indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)
- [Faiss 距離與度量](https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
