# 梯度消失與爆炸：長鏈、Jacobian與殘差路徑

先看精確標量乘積，再理解它對矩陣深網路提供的直覺。

## 導數連乘的結果

y=a^Lx時dy/dx=a^L。a=.5、L20約9.54e-7；a=1.5、L20約3325。第15例以double真實反向，對照解析乘積。它只是一條標量線性鏈，不將這個單數字當所有深網路的通用公式。

$$
\frac{\partial h_L}{\partial h_0}=J_LJ_{L-1}\cdots J_1
$$

矩陣乘積依方向與奇異值傳訊號，不只各元素平均；activation飽和、weight尺度與深度都影響。即使總norm看似正常，也可能部分方向已失去訊號。

## 如何觀察

每層activation分布、grad norm、零梯度比例與step前後參數差。grad=None先查路徑沒使用、斷圖或未反向；grad=0可能是正確局部導數。不能只將兩者都稱為「梯度消失」。追最早異常層，比在最後loss看到NaN才改lr更有效。

## 常見對策的角色

初始化改善初始尺度，activation選擇減少某些飽和，normalization控制部分統計，residual提供額外直接路，gated recurrent結構提供受控記憶。它們不是完全相同的修復；clipping控制大norm更新，不能創造不存在的梯度訊號。

## 輸入與目標也會影響

異常特徵尺度、極大target、錯誤loss縮放或不穩定exp／log都能造成爆炸。先回到小batch、FP32與eager，檢查finite；不要一開始就將所有grad任意clamp到很小數而不理解原因。

## 練習與解答

residual h_next=h+F(h)的Jacobian為I+J_F，當J_F近零仍有identity路徑；但若J_F在某方向約-I，也可能抵消，不能說residual保證永遠不消失。解答：用結構直覺產生假設，再由具體梯度與訓練實驗驗證。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/15_gradient_flow.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:15_gradient_flow.py -->

## 原始論文與官方來源

- [訊號傳遞與初始化](https://proceedings.mlr.press/v9/glorot10a.html)
- [Residual networks](https://arxiv.org/abs/1512.03385)
