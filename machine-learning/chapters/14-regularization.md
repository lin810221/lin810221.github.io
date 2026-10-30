# Ridge、Lasso與Elastic Net：用限制換取穩定性

比較L2收縮、L1稀疏與混合懲罰，理解尺度與超參數方向。

## 為什麼懲罰係數

特徵多、樣本少或欄位高度相關時，普通最小平方可能對小擾動很敏感。Ridge將係數往零收縮；Lasso可產生精確零；Elastic Net混合兩者。它們改變最佳化目標，可能增加train誤差卻減少未見資料誤差，是否有益由合理驗證判斷。

$$
L_{Ridge}=\lVert y-Xw\rVert_2^2+\alpha\lVert w\rVert_2^2
$$

$$
L_{Lasso}=\frac{1}{2N}\lVert y-Xw\rVert_2^2+\alpha\lVert w\rVert_1
$$

不同API的loss縮放未必相同，不能把相同alpha直接解讀為相同懲罰強度。兩者一般alpha越大限制越強；Logistic的C則是反方向，下一章再分清。

## 縮放與係數解讀

一欄用公尺、一欄用毫米，同樣coef大小代表不同效果。正則化前通常在Pipeline做StandardScaler，使懲罰的比較更合理。標準化後coef單位是每個train尺度，不是原始一單位。稀疏文字資料另需避免中心化成dense。

## 稀疏不是因果選擇

Lasso在相關欄位中可能挑其中一個；換split可能改選另一個。零係數表示此模型與此懲罰下未保留，不證明真實關係不存在。Elastic Net以l1_ratio控制L1/L2比例，可能在相關群中較穩定，仍需比較效能與選擇穩定性。

## 實作比較的界線

範例對同一固定split展示Ridge及Lasso的係數與holdout指標。這是機制比較，不應反覆看holdout調alpha；正式選擇放train CV，最後再評估。若CV前先fit scaler或selector，全流程仍可能洩漏。

## 練習與解答

調高Ridge alpha，係數norm通常下降；train error可能上升，val不必單調。若過大，預測可能接近只猜常數。解答：在對數尺度搜尋多個alpha，與dummy和未正則baseline比較，不以某次最大alpha分數較高就宣稱越大越好。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/06_regularization.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:06_regularization.py -->

## 官方來源與延伸閱讀

- [Ridge與Lasso](https://scikit-learn.org/1.9/modules/linear_model.html#ridge-regression-and-classification)
- [ElasticNet](https://scikit-learn.org/1.9/modules/linear_model.html#elastic-net)
