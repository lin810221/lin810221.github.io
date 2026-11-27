# 二元、多類與多標籤：不要讓答案格式決定錯任務

分清互斥類別、可同時成立的標籤與不同平均方式。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![回歸線與殘差；殘差是觀察值減預測值；低訓練誤差不等於新資料準確。座標圖為教學算例，沒有使用實測或臨床資料。](assets/figures/review-03-linear.svg)

> **圖解｜回歸線與殘差**：殘差是觀察值減預測值；低訓練誤差不等於新資料準確。座標圖為教學算例，沒有使用實測或臨床資料。

**本單元讀圖任務**：讀完「二元、多類與多標籤：不要讓答案格式決定錯任務」後，在圖上指出「殘差」的位置或對應關係；用本單元的一個例子說明它與「損失」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 三種不同的y

二元y[N]只有兩類；多類單選y[N]每筆只能一類；多標籤y[N,C]每一欄獨立是否成立。文章可同時屬於科技與商業是多標籤，水果只能選蘋果／香蕉／梨是單選。不要因為label是三欄one-hot就自動把任務當多標籤。

## 多類Logistic與softmax

多類模型可將每類線性分數用softmax正規化，機率加總1。支援multinomial的solver依目前API處理；不沿用已棄用的multi_class參數教學。One-vs-Rest則拆成各類與其餘的二元問題，與共同多類目標不同。

$$
P(Y=c\mid x)=\frac{\exp(z_c)}{\sum_k\exp(z_k)}
$$

## 多標籤的決策

每欄可有自己的機率與threshold，同一筆可以全部不選或選多個；classes與欄位順序必須保存。OneVsRestClassifier等wrapper可把支援的基礎分類器套用到多標籤，但還是要檢查訓練中每欄是否有正負例。非常稀有標籤可能無法在每fold形成可學問題。

```python
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
model=OneVsRestClassifier(LogisticRegression(l1_ratio=0,max_iter=1000))
# y_multilabel.shape == (N,C)
# model.fit(X_train,y_multilabel)
```

## 評估方式不可混用

macro每類同權，micro先合計計數，weighted依支持數，subset accuracy要求一筆所有標籤完全正確。多標籤只漏一個就subset錯，與每標籤正確率是不同難度。報告應列每類support，否則macro分數可能由幾個樣本極少類主導。

## 練習與解答

兩筆真值[[1,0],[1,1]]、預測[[1,0],[1,0]]，subset $\operatorname{accuracy}=.5$；四個位置有三個正確，逐標籤 $\mathrm{accuracy}=.75$ 。解答：兩者回答不同問題，不能只挑較大者。當任務從單選改多標籤，資料標註、loss、決策與指標都需一起重設，而不是只把模型輸出欄數改大。

## 官方來源與延伸閱讀

- [Multiclass與multilabel](https://scikit-learn.org/1.9/modules/multiclass.html)
- [Classification metrics](https://scikit-learn.org/1.9/modules/model_evaluation.html#classification-metrics)
