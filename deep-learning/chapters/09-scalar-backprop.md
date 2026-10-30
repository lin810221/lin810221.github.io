# 手算反向傳播：一個隱藏神經元的四個梯度

將forward數值保存，再沿每條依賴路徑回傳導數。

## 固定網路與數字

x=2，w1=.3、b1=-.1，a=w1x+b1=.5，h=sigmoid(a)；輸出ŷ=w2h+b2，w2=-.7、b2=.2，target=.8。loss=.5(ŷ-target)²。先列這些中間值，再算導數，比直接展開所有指數更容易核對。

## 從輸出往回

令e=ŷ-target，則dL/dŷ=e。輸出層dL/dw2=eh，dL/db2=e；對hidden傳回eh的係數需注意是e×w2，不是再次乘h。sigmoid的局部導數h(1-h)，最後乘x得到w1梯度。

$$
\delta_a=e\,w_2\,h(1-h),\quad
\frac{\partial L}{\partial w_1}=\delta_a x,\quad
\frac{\partial L}{\partial b_1}=\delta_a
$$

## 手算與Autograd對照

第3例以Python標量公式產生manual結果，再用double Tensor重算同一個圖，逐一比w1、b1、w2、b2。最大誤差應接近浮點精度。測的是導數，不拿「訓練有下降」代替梯度正確性證據。

## 為何要保存forward中間值

h已包含sigmoid結果，backward可直接用h(1-h)。大網路也會保存必要中間量；釋放或重新計算它們是記憶體策略，不改chain rule。若在backward前用in-place改掉需要的值，可能觸發版本錯誤，不能用.data繞過後假裝梯度仍可靠。

## 練習與解答

若w2=0，第一層透過這條路的梯度為0，但w2梯度eh仍可非零；下一步w2更新後又能傳訊號。若把loss的.5移除，全部導數乘2。解答：常數因子、mean分母與每條路徑都需一致，否則手算對照會整體差一倍或一個N。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/03_scalar_backprop.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:03_scalar_backprop.py -->

## 原始論文與官方來源

- [Autograd mechanics](https://docs.pytorch.org/docs/2.15/notes/autograd.html)
- [Back-propagation原理](https://www.deeplearningbook.org/contents/mlp.html)
