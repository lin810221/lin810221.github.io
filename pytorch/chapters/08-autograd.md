# Autograd：從手算偏導數到 backward

用一個只有單一權重的例子，對照計算圖、leaf Tensor 與梯度。

## 先用數字算一次

令 x=3、w=2、目標 t=10，預測為 6、平方誤差為 16。loss 對 w 的導數為 -24，因此小幅增加 w 應讓預測接近目標。梯度的正負描述局部變化方向，optimizer 的負號才把它轉成下降更新。

$$
L=(wx-t)^2,\qquad \frac{\partial L}{\partial w}=2(wx-t)x=-24
$$

## 哪些 Tensor 需要梯度

`w=torch.tensor(2.,requires_grad=True)` 是由你建立的 leaf。由 w 運算得到的 prediction 與 loss 有 grad_fn；一般 backward 後 leaf 的 `.grad` 被填入，中間非 leaf 預設不保存 `.grad`。看不到中間值的 grad 不代表它沒有參與反向傳播；需要觀察時可用 retain_grad。

## backward 的輸入與輸出

標量 loss 可以直接 backward；非標量輸出需要指定上游梯度，或先做符合目標的 sum/mean。`loss.mean()` 會同時改變目標縮放，影響梯度大小。`torch.autograd.grad` 可直接回傳指定輸入的導數，適合梯度檢查或高階微分；它與把值累加進 `.grad` 的使用方式不同。

## 可以觀察什麼

本章範例連續用相同 w 建立新的 forward，第一次梯度 -24，第二次累積為 -48，清成 None 再算回到 -24。數字完全可手算，適合先確認自己理解，再進入數百個參數的 MLP。記住「新計算圖」與「舊 `.grad` 是否清除」是兩件事。

## 練習與解答

若使用 SGD lr=0.01，第一次更新 w 是 `2 - .01*(-24)=2.24`，新預測 6.72、loss 約 10.7584。若 lr=1，w 變 26、loss 可能大幅增加；梯度正確不保證步長正確。修改範例加入 optimizer，核對權重和你的手算相同。不要以驗證集來挑每一批更新方向。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/04_autograd.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:04_autograd.py -->

## 官方來源與延伸閱讀

- [Autograd mechanics](https://docs.pytorch.org/docs/2.15/notes/autograd.html)
