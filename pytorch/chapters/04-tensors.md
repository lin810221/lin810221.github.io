# Tensor 的數值契約：建立、dtype、device 與共享儲存

學會辨認一個 Tensor 的四個基本屬性，以及資料轉換的成本。

## 數值之外還有什麼

Tensor 不只是巢狀 list。至少要讀 shape、dtype、device、requires_grad。`torch.tensor([1,2])` 通常推斷整數，而模型特徵多用 float32；分類索引使用 long。兩者都能印出數字，不表示可以交換使用。浮點 Tensor 才能參與一般可微分訓練。

## 常見建立方式

```python
import torch
x = torch.tensor([[1., 2.], [3., 4.]], dtype=torch.float32)
zeros = torch.zeros(2, 3)
ones = torch.ones_like(x)
indices = torch.arange(4, dtype=torch.long)
noise = torch.randn(2, 3, generator=torch.Generator().manual_seed(7))
print(x.shape, x.dtype, x.device, x.requires_grad)
```

`zeros_like` 等方式沿用參照 Tensor 的屬性，適合避免忘記 device；但仍要確認實際 dtype 是否符合任務。`torch.empty` 是未初始化空間，不能把讀到的任意值當作隨機分布。

## 轉換與拷貝的選擇

`.to(dtype=torch.float32)` 或 `.to(device)` 回傳轉換結果；通常要接回變數。`torch.tensor(existing)` 用來建立拷貝時應注意它會切斷原有計算歷史，需保留微分路徑時使用 Tensor 運算或 clone。NumPy 的 `from_numpy` 對可支援的 CPU array 會共用記憶體，任一側修改都可能影響另一側；跨 GPU 則需要搬移。

`x.item()` 只適合單元素 Tensor，轉成 Python 數字後不再有可微分路徑。做訓練日誌可以 `loss.detach().item()`；若把這個數字再拿來 backward，計算圖已不在。GPU 每批取 item 也可能帶來同步成本。

## 小心數值精度

float32 約有七位十進位有效數字，不代表任何運算都精確。大數加小數、很多項相加與不同順序都可能有誤差。測試用 `torch.testing.assert_close` 設合理容許值；標籤、索引與 shape 則應精確相等。需要梯度檢查時常用 double，並非所有訓練都改 float64。

## 練習與解答

建立特徵 `[8,4]` 與標籤 `[8]`，列出正確 dtype。解答：特徵 float32、類別索引 long。再比較 `a.detach()` 與 `a.detach().clone()` 是否共享數值，第 7 章會實測。讀入整數 JSON 特徵時明確指定 dtype，比期待自動推斷更可靠。

## 官方來源與延伸閱讀

- [Tensor API](https://docs.pytorch.org/docs/2.15/tensors.html)
- [Tensor attributes](https://docs.pytorch.org/docs/2.15/tensor_attributes.html)
