# L1、L2與weight decay：限制哪一種複雜度

從目標函數到實際更新，理解正則化尺度與參數分組。

## 在目標加入偏好

L2偏好較小係數，L1有促使部分係數零的幾何效果。它們限制特定參數化下的解，換一種等價重參數化不一定保留同樣懲罰。深網路有尺度對稱性與normalization，因此不能只用weight norm當普遍函數複雜度。

$$
L_{total}=L_{data}+\lambda\frac12\sum_k\theta_k^2\quad\Longrightarrow\quad
\nabla L_{total}=\nabla L_{data}+\lambda\theta
$$

## 更新規則仍需看optimizer

對基本SGD，某些L2與decay形式可相連；Adam的自適應縮放則使加進grad的L2與AdamW解耦decay不同。第20章已用零資料梯度核對，不應在這裡又把所有weight_decay都叫一樣的L2。

## 分母與超參數

loss使用mean或sum、資料量與累積方式會改data gradient相對懲罰強度。若每microbatch都加一次同樣λnorm，但整個群組只更新一次，可能重複算太多懲罰。先推整組目標，再寫實作；不能只複製一行penalty到每個迴圈。

## 哪些參數衰減

bias與norm affine是否decay可依方案設不同group，常見排除不是無條件規則。freeze參數、grad=None與optimizer參數清單也會影響是否更新。交付實驗記錄分組規則，否則兩個都寫AdamW的run仍可能有重要差異。

## 正則化不是資料清理

大weight不必是壞，少數pattern也不必是noise。先處理單位、label與切分；正則化無法修好洩漏或缺少代表性。透過train CV或val比較λ與任務指標，保留最後test，並觀察校準及子群錯誤。

## 練習與解答

同一effective batch拆4批，若loss_data每批正確sum/N、L2卻每批都加λ/2||θ||²，最後grad懲罰變4倍。解答：整組只加一次，或按明確權重分配，讓總目標相同。這種推導比「看起來loss下降」更能防止實作漂移。

## 原始論文與官方來源

- [Regularization](https://www.deeplearningbook.org/contents/regularization.html)
- [Decoupled decay](https://arxiv.org/abs/1711.05101)
