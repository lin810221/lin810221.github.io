# 線性融合與分數校準：何時分數才可以相加

比較每路 min-max 的簡易基線與跨查詢校準，認識單一路徑常數分數的陷阱。

## 線性融合的假設

加權分數假設各路分數經過可比較的轉換。最簡單可在每次查詢候選內 min-max，但它受候選深度與極端值影響，且跨 query 不可直接比較。對置信度、門檻或自動動作，通常需要用獨立標註資料校準，而不是把正規化結果叫機率。

$$
s'_r(d)=\frac{s_r(d)-\min s_r}{\max s_r-\min s_r},\qquad S(d)=\sum_r w_r s'_r(d)
$$

## 最大值等於最小值

若某一路只有一筆或所有候選分數相同，分母為零。課程定義該路的正規化分數全為0，表示沒有相對區別；也可採其他策略，但需明確記錄。無限值、NaN、負權重與所有權重皆零都應拒絕，不讓結果悄悄變成未排序列表。

## 候選缺席的定義

文件未出現在某一路，通常該路貢獻0，而不是猜一個原始分數。若能對候選聯集重新計算所有特徵，則已成為另一種重排流程，可得到更完整輸入，成本也不同。不要混淆未召回、真實低分與 Filter 拒絕三種情況。

## 如何選權重

以訓練/開發/保留測試分離的 qrels 調權重，避免對測試查詢反覆手調。依查詢類型分析代碼與自然語言是否需要不同策略。與 RRF 比較時固定候選與成本，並保留失敗例。單次漂亮排序不代表對整體分布校準成功。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 24_linear_fusion.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:24_linear_fusion.py -->

## 練習與解答

**請先嘗試：** 把 cosine 從 [-1,1] 轉成 [0,1]，就能當正確率嗎？

<details><summary>展開解答與判斷依據</summary>

不能，那只是尺度轉換，沒有建立分數與相關機率的經驗關係。需要獨立資料校準並檢查不同語言與查詢類型的可靠性；融合排序也應以 qrels 驗證。

</details>

## 官方文件與延伸閱讀

- [Elasticsearch RRF Retriever](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/retrievers/rrf-retriever)
- [Qdrant Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
