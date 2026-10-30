# 特徵工程與選擇：讓訊號可用，讓洩漏可見

結合領域定義、交互作用與選擇方法，避免只靠自動搜尋。

## 特徵是對問題的假設

原始日期可轉星期、月份或距離事件天數；金額可轉比例、成長或log；累計次數要有明確觀察窗。每種轉換都假設某種關係對預測有用。只要使用預測時不可知的未來總量，就算公式簡單也會洩漏。

## 非線性與交互作用

線性模型加入x²或x1×x2後，對原始輸入可表達非線性，但對展開後係數仍線性。PolynomialFeatures會增加維度與相關性，需要縮放、正則化與CV。樹能學一些分段交互，但不代表不需領域特徵或資料品質。

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures,StandardScaler
from sklearn.linear_model import Ridge
model=make_pipeline(PolynomialFeatures(2,include_bias=False),StandardScaler(),Ridge(alpha=1.))
# model.fit(X_train,y_train)
```

## 三種選擇方法

filter依統計關係選欄，例如SelectKBest；embedded依模型內部稀疏或重要性選；wrapper反覆訓練比較子集，例如RFE。全部都需放在訓練／CV邊界內，尤其使用y的方法。選擇結果依資料與模型，不是找到宇宙唯一的「真正重要」變數。

## 相關特徵與穩定性

高度相關欄位可分攤訊號，某次Lasso留A、另一次留B不一定互相矛盾。Permutation importance也可能因替代特徵存在而低估單欄作用。應記錄跨fold／seed的選擇穩定性、效能與成本，而非只貼一張重要性排名。

## 練習與解答

用全部y挑前10個特徵再CV為何不行？答案：每折驗證答案已參與選擇，應將selector放Pipeline。增加100個隨機欄位後train分數升高，能否說訊號更好？不能；比較獨立驗證與複雜度，隨機欄也可能讓模型記住雜訊。最終產物保留原欄位及轉換規則，才可一致推論。

## 官方來源與延伸閱讀

- [Feature selection](https://scikit-learn.org/1.9/modules/feature_selection.html)
- [Polynomial features](https://scikit-learn.org/1.9/modules/preprocessing.html#polynomial-features)
- [洩漏](https://scikit-learn.org/1.9/common_pitfalls.html)
