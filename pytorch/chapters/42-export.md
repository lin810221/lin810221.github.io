# 交付與匯出：state_dict、torch.export與ONNX入口

將模型格式、shape限制與執行runtime分清楚，避免把匯出成功當部署完成。

## 先選交付對象

同一Python程式重建模型可使用state_dict；需要可分析的運算圖則研究torch.export；跨runtime常會考慮ONNX與目標runtime的支援。格式檔案本身不包含完整服務：仍需前處理、欄位契約、版本、效能與監控。新教材以torch.export方向介紹圖匯出，TorchScript只用於辨認舊程式與遷移背景。

## 本課真實export往返

```python
from pathlib import Path
import tempfile, torch
from course_core import TinyMLP, export_roundtrip
model = TinyMLP().eval()
sample = torch.zeros(2,4)
with tempfile.TemporaryDirectory() as folder:
    error = export_roundtrip(model, sample, Path(folder)/'model.pt2')
    print(error)
```

在examples資料夾執行。它真的export、save、load，再使用loaded.module推論並比對同一輸入；CPU測試已覆蓋。`.pt2`是此流程的產物，與任意`.pt` state_dict並非單靠副檔名就可交換。

## shape與控制流限制

以[2,4]匯出不表示任意batch／任意feature都可用。動態維度需以dynamic_shapes／Dim等機制明確指定範圍並測試邊界。資料相依Python分支與不支援運算需按export限制處理，不可為了成功匯出悄悄改模型語意。eval模式與模型常數也要在匯出前決定。

## ONNX的選配路線

依最新版torch.onnx文件選擇exporter，安裝相容onnx／onnxscript及runtime，指定輸入輸出與動態shape，再在目標runtime比較logits、類別與誤差。此課沒有安裝或執行ONNX runtime，故只列交付流程，不把可匯出範例冒充已驗證的跨runtime部署。

## 交付驗收

至少一份golden input/output、極小與最大合理batch、dtype／欄位錯誤處理、模型hash與前處理版本、延遲與記憶體範圍。低精度／量化後再做數值與任務評估；格式轉換不是免費且無誤差的步驟。

## 練習與解答

把[2,4]輸入改[3,4]，若靜態匯出拒絕，不是weights壞了，而是shape契約不同。解答：保留靜態限制或明確匯出動態batch並測試；不能刪掉檢查後假裝支援。若Python與runtime分類相同但logits差很多，也應查數值，因為臨界樣本可能翻轉。

## 官方來源與延伸閱讀

- [torch.export指南](https://docs.pytorch.org/docs/2.15/user_guide/torch_compiler/export.html)
- [ONNX文件](https://docs.pytorch.org/docs/2.15/onnx.html)
- [2.10起TorchScript棄用背景](https://pytorch.org/blog/pytorch-2-10-release-blog/)
