# 重現與隨機性：seed是實驗條件的一部分

區分固定設定下的重跑、跨環境一致性，以及跨seed結果是否穩定。

## seed能固定什麼

模型初始化、資料打散、Dropout與生成採樣都使用隨機數。固定seed讓同一實作在同一環境更容易重跑；它不保證跨PyTorch版本、CPU／GPU或不同底層演算法逐位相同。GPU某些運算還涉及非確定性，應依官方說明選擇deterministic設定並衡量效能成本。本課只驗證CPU路徑。

## 亂數流也需要邊界

若新增一個畫圖用的randn就消耗全域RNG，後面的初始化可能改變。共用實作將資料生成和loader打散使用獨立Generator，降低無關操作的影響。模型與訓練仍有自身順序；這種分離是控制實驗的工具，不是完全切斷所有隨機依賴。

```python
import torch
g=torch.Generator().manual_seed(11)
first=torch.randn(4,generator=g)
torch.randn(100)  # 全域RNG不會改變g
g.manual_seed(11)
assert torch.equal(first,torch.randn(4,generator=g))
```

## 不只挑一個幸運seed

比較架構A、B時，預先決定seed集合、切分、訓練預算與主指標。在同一seed／split配對比較差值，比各挑最高分更能說明設定差異。記錄每次結果與平均、散布；標準差描述這組實驗的變動，並不自動等於資料母體或所有未來分布的不確定性。

$$
d_s=m_{B,s}-m_{A,s},\qquad
\bar d=\frac1S\sum_{s=1}^{S}d_s
$$

若指標是loss，差值負代表B較低；若是accuracy則方向相反。表格欄位要寫清楚，不能只用向上箭頭概括所有數字。

## 重跑清單要保存到哪裡

保留原始資料識別與切分索引、前處理、程式commit、Python／Torch完整版本、裝置、seed、超參數及最佳epoch。推論artifact只保留推論必要資訊；要精確續訓還需optimizer、scheduler、RNG與採樣進度。第66章會明確區分這兩種交付，本課範例不聲稱完整續訓。

## 如何寫可信的結論

「seed7在本機CPU合成資料上，validation loss降低」是可核對的觀察；「這個架構永遠優於其他架構」需要遠多於一個玩具實驗。若不同seed優劣反轉，應報告差異及成本，檢查資料大小、超參數預算與不穩定來源。不要因為測試能重跑，就將單次結果當成普遍結論。

## 練習與解答

固定seed後換GPU，結果有些微差異，是否表示程式一定有bug？答案：不一定。先比對版本、演算法與容許誤差，再檢查資料及執行順序。相反地，同環境、同輸入下存讀模型產生很大差異，應優先檢查eval模式與前處理，不能一概歸咎於隨機性。

## 原始論文與官方來源

- [PyTorch可重現性](https://docs.pytorch.org/docs/2.15/notes/randomness.html)
