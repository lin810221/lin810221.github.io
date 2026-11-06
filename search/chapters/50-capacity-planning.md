# 容量估算：原向量、量化、圖與複本都要算

從可驗算的 bytes 起步，明列未包含項目，避免把理想碼大小當總容量。

## 原始向量大小

N 筆、d 維、每元素 b bits，原始表示約為：

$$
B_{vector}=N d\frac{b}{8},\qquad
B_{planned}=(B_{vector}+B_{original}+B_{graph})\,C\,H
$$

C 是總 copies，包含 primary；H 是容量 headroom 倍數。GB=10^9 bytes，GiB=2^30 bytes。只報「1G」會讓不同單位與配置混淆，報告應同時保存精確 bytes。

## 圖與量化的粗估

本課 HNSW 圖用 N×M×2×4 bytes 作教學近似，沒有包含多層圖、allocator、ID、對齊與實作差異；正式容量以實測為準。量化成8bits可縮小表示，但若保留原float32向量作 rerank，還要加 N×d×4。PQ codes 也不等於一般 scalar quantization，需按 m 與 code bits 另算。

## 尚未包含的成本

倒排 posting、payload、B-tree/GIN、codebooks、文件本文、WAL、snapshot、merge 暫存、操作系統 cache、程序記憶體與重建時雙份索引，都可能很可觀。將 exclusions 與估算值一起回傳，避免看似精確的小數點掩蓋模型只覆蓋部分容量。

## RAM 與磁碟不是相同預算

索引可以將某些資料放磁碟並依賴 cache，但查詢 I/O、尾延遲與冷啟動會改變。某些量化配置還會保存原始向量；不要由 dtype 推論服務總 RAM。以實際 index bytes、RSS、page cache 與工作負載分別量測，再留升級與失效重建空間。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 29_capacity.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:29_capacity.py -->

## 練習與解答

**請先嘗試：** 一百萬筆768維，改8bits但保留float32原向量，向量相關容量是否只有原來四分之一？

<details><summary>展開解答與判斷依據</summary>

不是，碼約0.768GB，加保留原向量3.072GB，光兩者已約3.84GB，尚未含圖與 payload。若另有copies/headroom也要乘入。壓縮部分的比率不等於整個服務的容量比率。

</details>

## 官方文件與延伸閱讀

- [Faiss Indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)
- [Qdrant Indexing](https://qdrant.tech/documentation/manage-data/indexing/)
- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
