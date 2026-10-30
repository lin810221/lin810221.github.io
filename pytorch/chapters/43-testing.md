# 有意義的PyTorch測試：shape、梯度、續訓與數值等價

測行為與工程保證，避免把每行程式原封不動抄成測試。

## 哪些保證值得測

資料不洩漏、尾批平均正確、PAD不影響預測、參數確實更新、驗證不改梯度、快照不被後續更新污染、保存後輸出相同、受控續訓精確一致。這些測試能抓出實際錯誤；只測某函式呼叫幾次或某欄位等於寫死常數，不一定證明模型行為正確。

## 數值比較需有尺度

```python
import torch
actual = torch.tensor([.1 + .2])
expected = torch.tensor([.3])
torch.testing.assert_close(actual, expected, atol=1e-6, rtol=1e-5)
assert actual.shape == expected.shape
```

一般浮點使用容許值，shape、索引、label、樣本數精確比較。gradcheck用double與小平滑函數。訓練測試以明確可學的合成問題確認下降，避免外部模型下載與浮動API造成不穩定。

## 本課40項測試的範圍

測試包含Tensor／Autograd、資料契約與train-only scaler、collate／PAD、訓練／驗證、尾批累積、state_dict與resume、CPU profiler、compile eager backend與export往返。24個預設入口在另一cwd一起執行，測試攔截socket連線，確保預設流程不下載資料或呼叫服務。

```powershell
python -m unittest discover -s pytorch/examples -p test_examples.py -v
```

需先安裝2.15.0。本課CPU實測與CI使用同一鎖版；CUDA AMP、Inductor工具鏈、DDP真正通訊需額外環境，沒有用mock成功取代硬體驗證。

## 測試與benchmark分開

功能測試不把某台電腦50ms當通過條件。Profiler測事件確實存在，compile測輸出相容，並不測加速倍數。精確CPU resume在相同環境可要求零差；跨硬體則要先明確定義需要數值相近還是統計一致，不能一律複製容許值。

## 練習與解答

想驗證gradient accumulation，最有力的對照是複製同一模型，以完整batch與不等長microbatch各更新一次再比參數；只檢查loss有限不足。想驗證checkpoint，實際寫檔、重建、載入與推論，比只mock torch.save更能發現payload或weights_only的相容問題。

## 官方來源與延伸閱讀

- [Testing utilities](https://docs.pytorch.org/docs/2.15/testing.html)
- [Gradcheck](https://docs.pytorch.org/docs/2.15/notes/gradcheck.html)
