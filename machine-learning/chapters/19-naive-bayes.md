# Naive Bayes：條件獨立、平滑與文字分類

從Bayes公式理解高效基準，也看見機率假設的限制。

## 在每個類別內分開估特徵

由Bayes公式，P(c|x)與P(c)P(x|c)成正比。Naive假設給定類別後特徵條件獨立，將聯合分布拆乘積。文字單字並不真的獨立，但簡化模型仍常是有效基準；預測可用不代表假設成為真理。

$$
\hat c=\arg\max_c\left[\log P(c)+\sum_j\log P(x_j\mid c)\right]
$$

用log避免許多小機率相乘underflow。類別先驗與訓練樣本分布有關，資料抽樣比例改變時解讀要小心。

## 選對分布

MultinomialNB對非負計數／權重常見於文字；BernoulliNB用二元出現；GaussianNB以每類各特徵高斯分布處理連續值。不能把包含負值的StandardScaler輸出直接塞MultinomialNB，再用取絕對值掩蓋問題。TF-IDF常搭MultinomialNB作實用基準，但它不再是單純整數詞頻生成故事。

## 平滑避免零機率

某字在某類沒出現，若直接估0，乘積就全部為0。加α平滑給未見事件保留質量；α越大越向平滑分布靠近。搜尋α仍要在train內CV，詞表與IDF也放同一Pipeline，不先看全語料建立特徵。

## 本章文字示範

六段自寫英文短句分sport／software，TF-IDF加NB對兩段新句推論。這是小詞表機制，不是大語料準確率。中文需要斷詞或char n-gram策略，會在第43章補充；不要把英文預設token規則當中文萬用處理。

## 練習與解答

如果同義特徵高度相關，獨立假設可能重複計入證據，使機率過度自信。解答：以獨立保留資料檢查log loss／校準，不能只因accuracy不錯就相信每個.99。對負數特徵錯誤，先回到分布假設，選合適NB或改特徵，而非亂改dtype。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/09_naive_bayes.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:09_naive_bayes.py -->

## 官方來源與延伸閱讀

- [Naive Bayes](https://scikit-learn.org/1.9/modules/naive_bayes.html)
- [文字特徵](https://scikit-learn.org/1.9/modules/feature_extraction.html#text-feature-extraction)
