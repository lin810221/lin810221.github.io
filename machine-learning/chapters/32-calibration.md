# 機率校準：可靠度圖、Brier與Sigmoid／Isotonic

評估模型的信心是否有對應頻率，避免把排序能力當機率品質。

## 0.8應該代表什麼

一批分數接近.8的樣本，若長期約80%為正，這是校準直覺。它與分類accuracy不同：每筆都給.99與.51可能分類一樣，confidence品質不同。只有單筆事件結果，無法判斷該筆.8估計是否正確，需要跨樣本與資料分布檢查。

## 可靠度分箱與評分

reliability diagram把分數分箱，對照平均預測與實際正例率，並列每箱筆數。箱數太多在小資料會很不穩；空箱也要處理。Brier是機率平方誤差，Log loss重罰自信錯誤；它們受多種品質影響，不能把單一分數改善全歸因於校準。

$$
\mathrm{Brier}=\frac1N\sum_i(p_i-y_i)^2
$$

## 校準器也會學習

Sigmoid學平滑映射，Isotonic學單調分段映射，需要足夠資料。校準若用原模型已fit同樣資料的分數，可能樂觀。CalibratedClassifierCV用內部CV，讓校準看到未被相應base estimator訓練過的分數；前處理也要包在base Pipeline內。

## 本章真實執行

以StandardScaler+LinearSVC當base，method='sigmoid'、cv=3，實際fit校準ensemble，再在獨立holdout報Brier／log loss等。它不是mock，也不保證此資料上每個指標都進步。SVC原decision score可排序，經校準才進入明確機率輸出介面。

## 已fit模型與版本遷移

若使用已fit模型校準，要依目前API的FrozenEstimator等方式與獨立校準資料處理；不要照搬舊cv='prefit'模式並餵同一train。完整流程要預留校準與選threshold的資訊使用界線，不能把同一test反覆當校準、選模與驗收。

## 練習與解答

y=[1,0]、p=[.8,.3]，Brier=(.04+.09)/2=.065。若嚴格單調映射保留排名，AUC可能不變但Brier變。解答：排序與校準是不同維度。資料分布與正例比例改變後重新檢查，不因一次可靠度圖好看就永遠沿用相同信心解讀。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/21_calibration.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:21_calibration.py -->

## 官方來源與延伸閱讀

- [Probability calibration](https://scikit-learn.org/1.9/modules/calibration.html)
- [CalibratedClassifierCV](https://scikit-learn.org/1.9/modules/generated/sklearn.calibration.CalibratedClassifierCV.html)
