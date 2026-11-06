# IVF-PQ：分桶與壓縮帶來什麼誤差

把候選剪枝與向量量化分開理解，實際訓練一個小型 Faiss IVF-PQ。

## IVF 先縮小要掃的桶

IVF 以訓練資料學出 coarse centroids，向量分配到倒排列表；查詢只掃 nprobe 個列表。nlist 決定列表數，nprobe 控制查詢探索。若鄰近向量落在未掃的桶就會漏掉；訓練樣本不足、分布漂移或桶不均也會傷害效率與品質。

## PQ 再壓縮向量

Product Quantization 將 d 維分為 m 個子空間，各自學 codebook。每個子碼使用 b bits 時，理想碼大小約為：

$$
\operatorname{codeBytesPerVector}=\frac{m b}{8}
$$

這只是 codes，不含 ID、coarse centroids、codebooks、倒排結構、原向量與中繼資料。d 必須能被 m 整除；每個子空間有 2^b 個中心，需要足夠訓練資料。量化距離近似會改變名次，即使掃所有 IVF 列表也不必然恢復 Flat 排名。

## 入口的訓練選擇

本例用 2048 筆 32 維，16 個 coarse lists、m=4、每子碼4bits，避免拿十筆資料硬練大型碼本。提高 nprobe 觀察 Recall 與耗時，但不要把這個小例低 Recall 視為所有 IVF-PQ 都差；參數、訓練集與分布決定結果。

## 壓縮不是刪掉所有成本

若保留 float32 原向量作 rerank，主儲存仍需計入 N×d×4。也可能將壓縮向量放記憶體、原向量放磁碟，導致重排 I/O。容量報告應區分 codes、原向量、圖、payload、複本與暫存，而不是只宣傳 codes 的壓縮倍數。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 13_faiss_ivfpq.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:13_faiss_ivfpq.py -->

## 練習與解答

**請先嘗試：** nprobe=nlist 時，IVF-PQ 是否就與 Flat 完全相同？

<details><summary>展開解答與判斷依據</summary>

不一定。所有桶都掃到只消除了 coarse 候選剪枝，PQ 仍用量化表示估距。如果保留原向量，可對足夠候選作精確重排；是否恢復 top-k 仍取決於候選有沒有包含真值。

</details>

## 官方文件與延伸閱讀

- [Faiss Indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)
- [Faiss 官方文件](https://faiss.ai/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
