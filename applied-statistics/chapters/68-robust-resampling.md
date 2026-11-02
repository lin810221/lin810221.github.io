# 延伸D　延伸：非參數、重抽樣、缺失與多元模型

補足應用時常遇到的分岔，同時清楚標示超出原十章主線的範圍。

## 非參數不是無條件

Mann–Whitney比較兩組分布／隨機優越關係，在特定同形位置移動模型下才可簡化成中位差檢定。Wilcoxon signed-rank針對配對差值還有對稱等前提，不能只因「不是常態」就任意套用。Kruskal–Wallis也不會自動回答三個母體平均相等的同一問題。

## Bootstrap的單位

從已觀察樣本重抽、重算統計量以近似抽樣變動；iid樣本可按人重抽，配對需整對重抽，群集或時間依賴需相應方法。增加重抽次數降低模擬誤差，不補回失去的代表性、稀少尾端或錯誤測量。

```python
import numpy as np
from scipy import stats
x=np.array([2.,3.,4.,5.,7.,8.,9.,10.])
result=stats.bootstrap((x,),np.mean,confidence_level=.95,
    n_resamples=2000,method='percentile',rng=np.random.default_rng(7))
assert result.confidence_interval.low<result.confidence_interval.high
print(result.confidence_interval)
```

## 缺失不是一種固定值

完整案例、事前分數規則、模型或多重插補各有假設。MCAR、MAR、MNAR描述缺失機制，單靠已觀察資料通常無法證明MNAR不存在。平均補值可能壓縮變異並扭曲關聯；不能只為維持n就先補0或全體平均。

## 多元與GLM入口

加入多個X的OLS可描述條件關聯，但不自動消除混淆或選擇偏差；需檢查編碼、共線性、交互與模型。二元結果可考慮Logistic／GLM，係數在log-odds尺度，解讀不再是原分數每單位直線差。這些是延伸入口，不把本課簡單迴歸宣稱已覆蓋全部模型。

## 敏感度與解答

對合理處理政策或模型作預先規劃的敏感度分析，完整呈現哪些結論穩定、哪些改變。若只有某一種刪點或補值能顯著，不應只保留那個結果。可重現程式讓決策可審閱，統計判斷仍需要研究問題與資料機制。

## 參考與官方來源

- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [statsmodels 0.15文件](https://www.statsmodels.org/stable/)
- [SciPy bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)
