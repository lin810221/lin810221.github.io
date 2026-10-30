# 尺度與分布轉換：StandardScaler、RobustScaler與單位

知道哪些模型依賴距離與係數懲罰，哪些轉換會改變資料意義。

## 一個單位改變排名的例子

某特徵以公尺記錄，另一份改毫米，數值差1000倍。kNN的L2距離會被它主導；SVM與正則化線性模型也會受尺度影響。樹以閾值分裂，對單欄單調尺度轉換通常較不敏感，但缺失、數值精度與其他前處理仍有差異。

$$
z_{i,j}=\frac{x_{i,j}-\mu_j}{\sigma_j},\qquad
\mu_j=\frac1{N_{train}}\sum_{i\in train}x_{i,j}
$$

StandardScaler以train平均與變異數轉換。常態化到均值0與尺度1，不代表資料變成常態分布，也不會消除離群點。

## 選擇轉換方式

MinMaxScaler依train範圍縮放，新資料可超出0..1；RobustScaler用median／分位距，較不被極端值主導；log變換適合某些偏態正數但需處理零與負值；每列L2 normalize改的是向量長度，與每欄StandardScaler不同。先問你要保留大小還是方向。

```python
import numpy as np
from sklearn.preprocessing import StandardScaler,RobustScaler
train=np.array([[1.],[2.],[3.],[100.]])
print(StandardScaler().fit_transform(train).ravel())
print(RobustScaler().fit_transform(train).ravel())
```

## 稀疏資料與可解釋係數

對大稀疏矩陣中心化可能變成dense，記憶體暴增；需考慮with_mean=False或其他策略。標準化後係數是以轉換單位衡量，不能直接說「原特徵增加1會改變多少」。要回到原單位需結合scale與intercept，並注意相關特徵與因果限制。

## 練習與解答

train=[1,3,5]均值3，population標準差sqrt(8/3)，新值7的z約2.449。解答：只用train統計，即使val均值很不一樣也不重新fit。若每列normalize讓總消費大小消失，對依金額決策可能傷害訊號；縮放不是越多越好，應在完整Pipeline與CV比較。

## 官方來源與延伸閱讀

- [Preprocessing](https://scikit-learn.org/1.9/modules/preprocessing.html)
- [Pipeline與轉換](https://scikit-learn.org/1.9/modules/compose.html)
