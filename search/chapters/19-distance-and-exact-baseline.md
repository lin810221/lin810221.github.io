# 向量契約與 Exact 基準：先定義什麼叫鄰近

用同一個可查集合與距離函式建立正確答案，再衡量 ANN 的近似損失。

## 距離依賴表示契約

維度相同不保證可比較；模型、版本、前處理與正規化都必須相容。fixture-8d-v1 的八個特徵可直接閱讀，不能與另一個八維模型混用。輸入檢查拒絕 NaN、Infinity、錯誤維度與不符合要求的零向量，避免索引回傳難以解釋的結果。

## 三種常見度量

$$
\operatorname{cos}(q,x)=\frac{q^\top x}{\|q\|\|x\|},\qquad d_2(q,x)=\sum_j(q_j-x_j)^2
$$

內積與 cosine 越大越近，L2 越小越近。當 q 與 x 都 L2 normalize，squared L2=2−2cosine，所以排序一致；未正規化時不能套用這個關係。Faiss 的 L2 回傳平方距離，不需要再平方一次。

## Exact 也要先定資格

完整掃描所有可查向量得到 top-k，才是 ANN Recall 的參考。若查詢只允許 alpha active 文件，真值也只能從該集合計算，不能拿全域 top-k 當答案再用 Filter 補救。當可查資料只有三筆而 k=10，分母應取三；沒有任何真值時回報不適用，而不是編造滿分。

## 分數不是相關機率

cosine=0.8 不表示 80% 正確。不同模型、語言與查詢分布可有不同距離分布。Exact 只保證在既定表示與度量下找得最接近；若 embedding 沒學到任務概念，完美 Exact 也可能無關。表示品質在 Embedding 課程，索引近似損失在本課分開評估。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 10_exact_vectors.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:10_exact_vectors.py -->

## 練習與解答

**請先嘗試：** 兩個向量維度都為 768，是否能放在同一索引比較 cosine？

<details><summary>展開解答與判斷依據</summary>

必須先確認同一表示空間與 recipe。即使維度一致，不同模型的座標意義仍可能不同。採新 generation 重建並將查詢端一起切換，而不是只檢查 shape。

</details>

## 官方文件與延伸閱讀

- [Faiss 距離與度量](https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances)
- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
