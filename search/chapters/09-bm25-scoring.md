# BM25：詞頻、稀有度與文件長度如何影響名次

從可計算的公式理解排名，並分清原始 BM25、欄位權重與各引擎實作。

## 從詞頻到飽和

同一詞出現十次，不應總是比出現一次有十倍價值。BM25 的詞頻項逐漸飽和；k1 控制飽和曲線，b 控制文件長度正規化。參數應由評估集選擇，而不是看某一個查詢哪個分數最大。

$$
\operatorname{BM25}(q,d)=\sum_{t\in q}\log\left(1+\frac{N-n_t+0.5}{n_t+0.5}\right)\frac{f_{t,d}(k_1+1)}{f_{t,d}+k_1(1-b+b|d|/\operatorname{avgdl})}
$$

## 每個量代表什麼

N 是文件數，n_t 是包含詞 t 的文件數，f 是該文件詞頻，長度與平均長度都用同一 tokenizer 的 token 數。罕見詞通常得到較高 IDF；長文較容易碰巧含有查詢詞，因此引入長度修正。式子採正值 IDF 版本；本課手刻函式對重複 query token 去重，並非完整 query-term-frequency 模型。

## 分數不能跨系統硬比較

SQLite FTS5 的 bm25 較小較好，且有自己的 IDF 處理與欄位加權；Elasticsearch 使用其 similarity 與 shard 統計。範例中的正值手算用來解釋機制，不能宣稱數字與任何引擎逐位相同。不同 query 的 BM25 值也通常不是校準後的相關機率。

## 有用的觀察方法

先固定 tokenizer 和文件集合，改動一篇文件的詞頻與長度，再比較名次。加入大量背景文件會改變 IDF，原排名可能變動。標題 boost 可以改善標題匹配，也可能讓充斥關鍵字的標題壓過真正有用本文；需搭配盲測 qrels，並檢查零結果與錯別字案例。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 04_bm25.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:04_bm25.py -->

## 練習與解答

**請先嘗試：** b=0 時，長文件還會因為長度而被這個詞頻項懲罰嗎？

<details><summary>展開解答與判斷依據</summary>

不會，長度因子退化成 1；但詞頻與 IDF 仍影響結果。b=1 代表完整使用相對長度，不表示一定最佳。分別觀察固定詞頻、改變長度的實驗，才能隔離這個參數的作用。

</details>

## 官方文件與延伸閱讀

- [Elasticsearch Similarity](https://www.elastic.co/docs/reference/elasticsearch/index-settings/similarity)
- [SQLite FTS5 官方文件](https://www.sqlite.org/fts5.html)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
