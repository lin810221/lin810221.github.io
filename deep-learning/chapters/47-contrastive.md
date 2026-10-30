# 表示與對比學習：讓相似的定義來自任務

從positive pairs、negative candidates到可微分的InfoNCE目標。

## 學相似之前先定義相似

同一影像不同合理增強、同意句或相同實體可作positive，但規則要符合任務。不相關不一定是真negative，同topic不同樣本也可能false negative。標註／增強選擇定義表示偏好，loss本身不會替你理解哪些關係有用。

## In-batch候選與溫度

normalize後的向量內積形成相似度矩陣，對角為正配對，其他作候選負例；temperature縮放logits。較低溫增加相對差異與某些梯度，不保證所有情況更好。小batch的負例種類有限，需配合資料設計。

$$
\ell_i=-\log\frac{\exp(s(a_i,b_i)/\tau)}{\sum_j\exp(s(a_i,b_j)/\tau)}
$$

## 實作與collapse檢查

第33例雙向平均a→b與b→a，實際對兩組向量backward，列grad norm。所有向量相同時logits相同，loss=logN；這是數學核對，不表示collapse已被所有目標自動排除。零向量cosine語意不明，本課直接拒絕。

## 評估不只訓練loss

用下游分類／檢索、linear probe、近鄰、跨來源與多語等按任務評估。表示score不是正確率，維度相同不表示空間相同。若之後微調，索引與cache都可能要重建；embedding完整應用可讀既有獨立課。

## 練習與解答

N4且所有logits相等，positive機率1/4、loss約1.386。解答：如果把loss報成「相似度86%」就搞錯量。新增負例可能使loss比較基準改變，不能跨不同candidate數直接以原始loss大小判斷表示品質。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/33_contrastive.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:33_contrastive.py -->

## 原始論文與官方來源

- [SimCLR原始研究](https://arxiv.org/abs/2002.05709)
- [表示學習](https://www.deeplearningbook.org/contents/representation.html)
