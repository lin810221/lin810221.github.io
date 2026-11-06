# Benchmark、p50 與 p95：量測一個可比較的工作負載

建立真實 Faiss 計時入口，同時把本機核心耗時與服務端到端延遲分開。

## 定義量測範圍

本課入口量測暖機後單一 Faiss index.search，使用固定 seed、維度、queries 與 OMP threads。它不包含模型 encode、網路、序列化、Filter、來源 hydration、排隊或重排。報告會明寫範圍，不將微秒級小例拿來宣稱整個搜尋服務能達相同延遲。

## 百分位不是平均

p50 表示中間位置，p95 描述較慢尾端；少量查詢的百分位不穩定。保存逐 query timing、重複次數與原始排序方法，避免只取最快一次。冷啟動、cache、CPU 頻率、背景工作與執行緒數都會影響結果，測試前後應記錄環境。

## 服務壓測要包含排隊

固定併發與固定到達率是不同負載模型。若只等每個請求完成再送下一個，可能漏掉高負載排隊的尾端問題。需觀察吞吐、失敗率、timeout、queue time、CPU、RAM、I/O 與索引更新競爭。超出容量時要有背壓與拒絕，而非無限排隊。

## 品質與耗時一起報

每組參數同時保存 ANN Recall、qrels 指標、候選數與延遲。減少候選或降低 efSearch 可能更快但漏資料，沒有品質下限的最快結果沒有產品意義。重複測量後再選滿足 SLA 的設定，不因一個漂亮數字定案。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 30_benchmark.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:30_benchmark.py -->

## 練習與解答

**請先嘗試：** 本機單查詢 p95 很低，為什麼上線後仍 timeout？

<details><summary>展開解答與判斷依據</summary>

上線增加 encode、網路、連線池、排隊、Filter、payload、來源取回與併發，還可能有冷快取和背景 merge。應分段 trace 端到端路徑並以實際到達率測試，不能只重跑核心 search microbenchmark。

</details>

## 官方文件與延伸閱讀

- [Faiss 官方文件](https://faiss.ai/)
- [Faiss Indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
