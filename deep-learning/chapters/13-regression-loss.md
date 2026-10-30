# 回歸損失：MSE、MAE與Huber的梯度偏好

將相同殘差送入不同目標，觀察大誤差受到多少懲罰。

## 殘差與單位

e=prediction-target，MSE平均平方、MAE平均絕對值。MSE的梯度隨誤差變大，MAE除了零點約定外為符號。目標單位、尺度與outlier來源都會影響選擇，不能只說一個loss永遠較穩健。

$$
L_{MSE}=\frac1N\sum_i e_i^2,\qquad L_{MAE}=\frac1N\sum_i|e_i|
$$

## Huber的折衷

小殘差用平方，大殘差用線性增長，delta控制切換尺度。delta也有target單位，資料改單位需重新考慮。SmoothL1與Huber在某些參數下有縮放關係，不把API不同名稱當完全相同公式。

$$
\ell_\delta(e)=\begin{cases}\frac12e^2,&|e|\le\delta\\\delta(|e|-\frac12\delta),&|e|>\delta\end{cases}
$$

## 手算同一批

pred=[0,2,5]、target=[1,2,3]，殘差[-1,0,2]。MSE=5/3，MAE=1，Huber(delta1)=2/3。第7例同時輸出每個prediction的梯度，核對mean分母。大錯誤會在不同目標中有不同更新影響。

## Loss與評估指標

用Huber訓練仍可報MAE、RMSE與signed residual。只報train loss無法判斷未見表現；若target有log變換，最後仍需在原單位評估。權重、missing target或多輸出會改reduction分母，先定義契約再算。

## 練習與解答

把全部target與prediction乘100，MAE乘100、MSE乘10000；Huber若delta不變，部分樣本會跨分段，不能只說乘固定倍數。解答：loss、梯度、學習率與單位要一起考慮。若pred[N,1]對target[N]，先修shape，不用換loss掩蓋廣播錯誤。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/07_regression_losses.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:07_regression_losses.py -->

## 原始論文與官方來源

- [Regression loss functions](https://docs.pytorch.org/docs/2.15/nn.html#loss-functions)
