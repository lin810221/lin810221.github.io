# 信心、校準與分布外資料：高分不等於可靠

理解機率品質、溫度縮放與分布移動，避免把softmax最大值視為安全保證。

## 分類正確與機率正確

模型將所有樣本預測為正類：若其中八成真的為正，輸出0.8和0.999的分類結果相同，但機率品質很不同。校準關心宣稱某信心的樣本群是否有相近正確率。分箱圖還需樣本量；只有兩筆的箱子非常不穩定，不宜過度解讀。

## 兩個可以手算的分數

二分類Brier取機率與0／1標籤的平方差平均，NLL對給真實類別極低機率的錯誤有很大懲罰。若y=1，p=.8的Brier為.04；p=.1則為.81。評估時也看分類、類別分組與資料切片，單一平均可能掩蓋少數群組的失敗。

$$
\operatorname{Brier}=\frac1N\sum_i(p_i-y_i)^2,\qquad
\operatorname{NLL}=-\frac1N\sum_i\log p_i(y_i)
$$

這裡Brier是二分類單一正類機率的定義；多類別版本通常還對類別加總，報告時須寫明慣例。

## 溫度縮放只改一個正數

將已訓練模型凍結，在另外保留的校準資料上以NLL估T>0，再用softmax(z/T)。T較大讓分布平緩；它保留同一筆logits的argmax，所以通常不改top-1分類結果，無法修好原本分類錯誤。校準資料可從validation另分；不要用最終test調T。

$$
p_T(c\mid x)=\frac{\exp(z_c/T)}{\sum_j\exp(z_j/T)},\qquad T>0
$$

```python
import torch
z=torch.tensor([[2.,0.,-1.]])
p1=(z/1.).softmax(-1)
p2=(z/2.).softmax(-1)
assert p1.argmax()==p2.argmax()
assert p2.max()<p1.max()
```

## OOD沒有由softmax自動解決

訓練只見過水平／垂直亮帶，對自然照片仍會被迫分到這兩類；很大的最大機率不表示看過相似資料。需要事先定義分布外情境、適合的驗證集合與拒答／人工處理政策，評估偵測錯誤率與成本。溫度縮放在一個分布有效，也不保證對另一分布仍校準。

## 練習與解答

校準後accuracy不變，NLL下降，是否沒有改善？答案：機率品質可能改善，對依信心採取行動的流程有意義；應用保留資料驗證。若只看到ECE下降，也需檢查分箱選擇、NLL及樣本數，不能單憑一個分箱數字宣布可靠。

## 原始論文與官方來源

- [溫度縮放原始研究](https://arxiv.org/abs/1706.04599)
- [分類目標與logits](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html)
