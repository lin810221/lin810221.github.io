# 計算圖生命週期與梯度累積：為什麼需要 zero_grad

釐清每次 forward 的圖、反向保存的中間量，以及跨 batch 的梯度狀態。

## 三種狀態分開看

參數是長期保存的 leaf；forward 建立本輪計算圖；`.grad` 是參數上的梯度緩衝。一般 backward 後會釋放用於反向計算的中間量，參數與已累積梯度仍存在。下一批 forward 建立新圖，但不會自動清除舊 grad。

## 正確的最小迴圈

```python
import torch
w = torch.nn.Parameter(torch.tensor(2.))
optimizer = torch.optim.SGD([w], lr=.01)
for target in [10., 9.]:
    optimizer.zero_grad(set_to_none=True)
    loss = (3*w - target).square()
    loss.backward()
    optimizer.step()
print(w.detach())
```

zero_grad 在每次有效更新開始清除緩衝；backward 將這次梯度加入；step 讀取梯度。`set_to_none=True` 讓未得到梯度的參數維持 None，與數值全零並非所有 optimizer 情境都等價。不要使用 `if p.grad` 判斷 Tensor，應檢查 `p.grad is None`。

## 為什麼重複 backward 會失敗

對同一個 `loss` 呼叫兩次 backward，可能因保存量已釋放而失敗。通常應重新 forward。`retain_graph=True` 是需要重用同一圖做多次反向時的工具，不是所有錯誤的修復開關；不必要保留圖會增加記憶體。若想對導數再微分，則涉及 create_graph，目的也不同。

## 日誌不要把圖留住

`history.append(loss)` 可能讓 Python 容器一直引用圖。日誌使用 `loss.detach().item()`；需要批次預測來計算非微分指標時先 detach，必要時搬到 CPU。也不要把每批 loss 相加留到整個 epoch 才 backward，除非你刻意設計並承擔保存所有圖的成本。

## 練習與解答

梯度累積是否永遠是 bug？不是；第 36 章將多個 microbatch 的正確加權梯度合成一次更新。差異在於你清楚知道有效群組何時開始、loss 如何縮放及何時 step。練習把上述 zero_grad 移除，比對第二輪 `.grad`：它同時包含前一輪導數，與逐批 SGD 不同。

## 官方來源與延伸閱讀

- [Autograd 圖的重建與保存](https://docs.pytorch.org/docs/2.15/notes/autograd.html)
- [optimizer 梯度操作](https://docs.pytorch.org/docs/2.15/optim.html)
