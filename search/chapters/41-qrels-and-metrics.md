# Qrels、Recall、MRR 與 nDCG：別把兩種正確混在一起

同時量測 ANN 是否接近 Exact，以及搜尋結果是否真的相關。

## 兩份不同的答案

ANN 的 ground truth 是相同表示、metric 與資格內的 Exact top-k；搜尋品質的 qrels 是人或受控流程標註的 query-document relevance。前者滿分不代表後者滿分。表示不合任務時，Exact 找到的鄰居可能仍無關。

$$
\operatorname{ANNRecall@k}=\frac{|A_k\cap E_k|}{|E_k|},\qquad
\operatorname{DCG@k}=\sum_{i=1}^{k}\frac{2^{rel_i}-1}{\log_2(i+1)}
$$

## 分母與空集合

可查資料不足 k 時，Exact 真值分母是實際數量；沒有任何真值時回不適用。nDCG 以同 qrels 的理想 DCG 正規化，沒有正相關文件時同樣要明訂政策。本課回 None 並讓匯總報告排除、另列數量，不把它們自動算成100%。

## 其他指標

MRR 看第一個相關結果的倒數名次，適合只需一個答案的查詢；Recall 看召回覆蓋，Precision 看回傳中相關比例。分級 relevance 可用 nDCG 區分非常相關與部分相關。未標註文件不必然無關，若採當0處理要揭露評估集完整度。

## 避免資料洩漏

開發集調參、保留集做最後報告；同源近重複 query 或版本文件分散兩邊會使結果過度樂觀。每個 qrel 包含 query_id、doc_id、tenant、標註版本與判準。評估只使用該主體可查集合，不因有 qrel 就越過授權 Filter。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 25_evaluation.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:25_evaluation.py -->

## 練習與解答

**請先嘗試：** ANN Recall=1，使用者仍說結果很差，先查哪裡？

<details><summary>展開解答與判斷依據</summary>

索引近似已接近既定距離真值，應檢查表示、query intent、tokenization、來源完整度、融合與人工相關性。不要再把 efSearch 無限拉高當主要改善方法。

</details>

## 官方文件與延伸閱讀

- [Faiss Indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)
- [Faiss 距離與度量](https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
