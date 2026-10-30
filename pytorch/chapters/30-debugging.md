# 訓練除錯實務：一個batch、hooks與梯度診斷

用最小可重現問題定位錯誤，讓每個實驗都能排除一種原因。

## 從能否擬合一批開始

固定一個小batch，關掉複雜augmentation，先讓小模型反覆學它。如果loss完全不動，查參數註冊、grad、lr、loss契約與step；若能很快擬合，資料管線至少有基本學習訊號，再進入完整split。這是診斷，結果不能當泛化成績。

## 逐層檢查有限值與尺度

```python
import torch
from course_core import TinyMLP
model = TinyMLP(dropout=0)
handles = []
def inspect(module, inputs, output):
    print(type(module).__name__, tuple(output.shape), bool(torch.isfinite(output).all()))
for layer in model.network:
    handles.append(layer.register_forward_hook(inspect))
model(torch.ones(2,4))
for handle in handles:
    handle.remove()
```

hook只做觀察，不把output長期存入list保留圖；完成移除，避免後續訓練印出大量資訊或影響效能。真實模型可能回傳tuple/dict，需按介面處理，不能把這個Tensor-only hook原封不動套到所有架構。

## 梯度與更新分別量測

backward後看grad是否存在、是否finite與norm；step前後用detach().clone比較參數差值。gradient大不等於update大，AdamW會使用狀態與縮放；相反地某些參數本輪grad為零，動量仍可能讓它改變。需要比較實際變化，而不是只印loss。

## 調整的順序

先關AMP、compile、DDP回到CPU eager，固定資料與seed。找到最早壞值或最小shape錯誤，再逐一恢復功能。若CPU正確GPU不正確，檢查裝置、精度、非同步錯誤位置與不支援運算。不要同時修改多項來讓程式「看起來好了」。

## 練習與解答

模型train loss下降、val明顯升高：查過擬合、資料分布與前處理，不能直接判斷是optimizer壞了。兩者都完全不動：查學習訊號與更新。只有batch_size=1失敗：查無參數squeeze、BatchNorm及shape假設。解答要附最小輸入與expected/actual shape，才有可追蹤的證據。

## 官方來源與延伸閱讀

- [Module hooks](https://docs.pytorch.org/docs/2.15/notes/modules.html)
- [Anomaly detection](https://docs.pytorch.org/docs/2.15/autograd.html)
