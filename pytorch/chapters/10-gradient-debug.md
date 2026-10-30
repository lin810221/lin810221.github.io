# 梯度除錯：chain rule、gradcheck 與 in-place 操作

以可手算與數值差分的實驗，區分圖被切斷、梯度為零與數值不穩。

## 梯度為 None 與零不一樣

None 常表示還沒 backward、不是被追蹤的 leaf、路徑沒用到該參數或剛被 zero_grad 清除。零可能是正確導數，例如 ReLU 負區間。先檢查 requires_grad、is_leaf、grad_fn 與 loss 是否真的連到該參數，再調 learning rate。

## 中央差分當第二種證據

$$
\frac{\partial L}{\partial w}\approx\frac{L(w+\epsilon)-L(w-\epsilon)}{2\epsilon}
$$

epsilon 太大是截斷誤差，太小是浮點相減誤差。以 double、平滑函數與小張量測試，可避免把 ReLU 折點的不連續判成 Autograd 錯誤。gradcheck 不是在大型隨機 Dropout 訓練圖上隨意執行。

```python
import torch
x = torch.tensor([.2, -.4], dtype=torch.double, requires_grad=True)
print(torch.autograd.gradcheck(lambda v: (v.sin()*v).sum(), (x,)))
```

## 三個會切斷路徑的行為

先 item 再用 Python 數字重建 loss；將中間值 detach；把 Tensor 轉 NumPy 計算再包回 Tensor。這些操作可能讓數值看起來正常，卻無法回傳原參數的導數。若確實需要不可微分的流程，應明確設計訓練目標，而非用 requires_grad=True 偽造原本的連接。

## in-place 與 anomaly detection

以 `_` 結尾的 add_ 等操作直接修改儲存。若 backward 需要修改前的值，Autograd 的版本檢查會報錯。優先改成 out-of-place；更新參數由 optimizer 或 no_grad 區塊管理。除錯可在小範例使用 `with torch.autograd.detect_anomaly():` 包住 forward/backward，取得更多位置資訊；它有額外成本，不必一直開在正式訓練。

## 練習與解答

寫 `loss = torch.tensor(old_loss.item(), requires_grad=True)` 後 backward，為何模型 grad 是 None？答案：你創造新的 leaf，它只知道自己的導數，不知道 old_loss 的來源。保留原 loss 直接 backward，日誌另存 detach().item。再試試讓參數完全沒用進 forward，觀察即使 loss 有 grad_fn，該參數仍可沒有 grad。

## 官方來源與延伸閱讀

- [Autograd mechanics](https://docs.pytorch.org/docs/2.15/notes/autograd.html)
- [Gradcheck mechanics](https://docs.pytorch.org/docs/2.15/notes/gradcheck.html)
