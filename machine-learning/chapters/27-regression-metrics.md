# 回歸評估：MAE、RMSE、R²與殘差單位

理解指標的分母、尺度與負分數，避免只報一個數字。

## 誤差必須有單位

若y是分鐘，MAE與RMSE也以分鐘解讀；MSE單位是分鐘平方。不同target尺度的MSE不能直接比較。多目標回歸需說明每個輸出的權重與單位，不能隨便平均金額與比例而假裝同一代價。

$$
MAE=\frac1N\sum_i|y_i-\hat y_i|,\qquad
RMSE=\sqrt{\frac1N\sum_i(y_i-\hat y_i)^2}
$$

RMSE對大誤差更敏感；MAE也不是對所有離群資料無影響，只是懲罰增長方式不同。

## R²可以是負數

R²以平方誤差相對常數均值基準描述解釋程度。模型比該評估集的均值預測還差時可以負，不需要強行clip到0。y完全常數時有特殊邊界，API可能依force_finite政策處理，報告需知道這不是一般變異情境。

$$
R^2=1-\frac{\sum_i(y_i-\hat y_i)^2}{\sum_i(y_i-\bar y)^2}
$$

## 手算與目前API

y=[1,2,3]、pred=[1,2,5]，MAE=2/3、MSE=4/3、RMSE=sqrt(4/3)，R²=1-4/2=-1。本課使用root_mean_squared_error，不以舊版MSE squared=False介面作主線。指標函式先驗證同shape，避免[N,1]與[N]的隱含廣播。

## 殘差分布與百分比陷阱

看誤差分位數、最大錯誤、signed bias與子群，不只全體平均。MAPE遇到y接近0會極大，且相對誤差對高低值權重不同；log target需檢查零／負值與轉回原單位後偏差。挑選指標要依任務，不因漂亮百分比就使用。

## 練習與解答

把目標從公尺改公分，MAE與RMSE乘100，MSE乘10000，R²若預測同步換單位則不變。解答：模型改善必須在同單位與同資料比較。再以DummyRegressor的train mean作真正可部署基準，不能偷用test mean生成你的正式預測。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/16_regression_metrics.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:16_regression_metrics.py -->

## 官方來源與延伸閱讀

- [Regression metrics](https://scikit-learn.org/1.9/modules/model_evaluation.html#regression-metrics)
