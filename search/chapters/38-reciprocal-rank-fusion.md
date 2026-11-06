# RRF：不用混比分數，也能融合多路排名

從排名而非原始分數融合候選，處理去重、權重與缺席分支。

## 為什麼不用直接相加

BM25、cosine、sparse inner product 的尺度與分布不同，直接加總會讓某一路因數值大而主導。RRF 使用每路名次，減少對原始分數校準的依賴，但仍受候選深度、分支品質與常數影響。它是穩健基線，不是永遠最佳排序器。

$$
\operatorname{RRF}(d)=\sum_{r\in R_d}\frac{w_r}{c+\operatorname{rank}_r(d)}
$$

## 名次與參數

名次從 1 起算；c≥0 控制頭部名次差距，與最後回傳 k 不同。文件在某一路缺席就不加該路分數；權重0的分支應完全不貢獻，不能把它的獨有文件以零分加入結果。每路重複 ID 是輸入錯誤，先去重或拒絕，而不是重複加分。

## Candidate window 的影響

各路只取前十與前百，RRF 的候選聯集會不同。前十之外的文件即使非常相關，也無法被融合救回。更大的視窗增加召回機會與成本；評估時將 candidate budget、c、weights 與最後 k 一起記錄，不只保存 fusion=rrf。

## 本課與服務內建 RRF

Python 入口是明確的一基排名加權公式；Qdrant Fusion 與 Elasticsearch retriever 有各自 API、預設與版本行為，不能要求數值逐位相同。比較時先確認分支候選與資格一致，再評估排名與相關性。融合後仍須回來源檢查最新文件，避免把過期候選呈現。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 23_rrf.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:23_rrf.py -->

## 練習與解答

**請先嘗試：** 一條無關分支的 weight=0，還應讓它獨有的文件出現在最後嗎？

<details><summary>展開解答與判斷依據</summary>

不應，零權重表示這條分支沒有召回貢獻；範例直接跳過。若產品另有候選補齊策略，應單獨命名並驗收，不能悄悄混入 RRF 的定義。

</details>

## 官方文件與延伸閱讀

- [Elasticsearch RRF Retriever](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/retrievers/rrf-retriever)
- [Qdrant Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
