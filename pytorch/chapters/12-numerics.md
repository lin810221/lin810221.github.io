# 數值穩定性：NaN、Inf、mask 與精度

先找出第一個失效的運算，再決定是否需要更高精度或不同公式。

## 問題可能比 backward 更早

loss=NaN 的原因可以是輸入缺失、除以零、log(0)、overflow 或學習率太大。先查資料與 forward 中間量，再查梯度。用 `torch.isfinite(tensor).all()` 找第一個非有限值；只把最後 loss 的 NaN 改成零，會隱藏上游問題，也可能讓模型停止學習。

## 用穩定的運算式

分類使用原始 logits 搭配 CrossEntropyLoss，二元分類使用 BCEWithLogitsLoss，比先手寫 exp／sigmoid 再 log 容易保持穩定。對數機率可用 log_softmax 或 logsumexp。數學等價的式子，在有限精度中未必有同樣表現。

```python
import torch
z = torch.tensor([1000., 1001.])
print(torch.exp(z).isfinite())
print(torch.logsumexp(z, dim=0))
denominator = torch.tensor([0., 2.])
valid = denominator.ne(0)
result = torch.zeros_like(denominator)
result[valid] = 1. / denominator[valid]
print(result)
```

## mask 要在危險運算之前

如果先 `1/x` 得到 Inf，再用 mask 去掉結果，Autograd 仍可能遇到先前的無效運算。上述範例只對有效分母做除法。Padding 的平均也要以有效 token 數當分母，並拒絕整列全 mask；不能只填零後直接 mean 所有位置。

## 精度與比較

float16 的範圍與有效位數不同於 bfloat16、float32；AMP 會依運算選擇型態，不代表所有 Tensor 都改 half。不同硬體與 reduction 次序可有微小誤差。數值測試設定 atol、rtol 時要連回任務尺度；比較分類標籤則用精確一致，不把容許值套在所有東西上。

## 練習與解答

模型第一個 batch 就 NaN：先看 x/y、標準差、loss 的輸入契約；第十個 epoch 才 NaN：再看梯度範數、更新幅度與中間 activation。解答順序是縮小到一批並固定 seed，記錄首次壞值的位置，確認公式與 dtype，再嘗試降低 lr 或 gradient clipping。clipping 處理大梯度，不能修好本來就無效的標籤或除零。

## 官方來源與延伸閱讀

- [Numerical accuracy](https://docs.pytorch.org/docs/2.15/notes/numerical_accuracy.html)
- [Autograd 與無效運算](https://docs.pytorch.org/docs/2.15/notes/autograd.html)
