# 常用層與 shape：Linear、Conv2d、Embedding 與正規化

把每一層當作有明確輸入輸出規格的數值運算。

## Linear 的最後一軸

nn.Linear(F,C) 將最後一軸 F 變成 C。`[N,F]→[N,C]`，`[N,T,F]→[N,T,C]`；它不會自動把時間軸平均。權重儲存 `[C,F]`，bias `[C]`。加入 ReLU 等非線性，才能讓多層線性網路超越單一線性映射的表示能力。

## Conv2d 與空間尺寸

一般 Conv2d 輸入 NCHW。輸出高度由 kernel、padding、stride、dilation 決定；寬度同理。不要只照別人的 Flatten 後尺寸，應自己推算或用一個 dummy batch 檢查。

$$
H_{out}=\left\lfloor\frac{H+2P-D(K-1)-1}{S}+1\right\rfloor
$$

本課 8×8、kernel3、padding1、stride1 保持 8×8，輸出4個 channel，Flatten 是256，而不是64。第26章完整例子直接驗證這個尺寸。

## Embedding 是查表

tokens[N,T] 的 dtype 為 long，Embedding(V,D) 輸出 `[N,T,D]`。token ID 是索引，不是連續數值特徵。ID 必須落在詞表範圍，padding_idx 指定特殊列。本課不下載 tokenizer 或語言模型，而用明確的手工詞表展示這個操作。

## Dropout 與正規化的狀態

Dropout 在 train mode 隨機遮蔽，eval 關閉；BatchNorm 在訓練及驗證使用統計的方式不同。LayerNorm 則依指定尾部維度正規化，不使用相同的 running mean 機制。batch_size 小、資料分布不同時，不能只因為都叫 normalization 就互換。

```python
import torch
from torch import nn
image = torch.zeros(2,1,8,8)
conv = nn.Conv2d(1,4,3,padding=1)
print(conv(image).shape)  # [2,4,8,8]
ids = torch.tensor([[1,2,0]])
print(nn.Embedding(8,4,padding_idx=0)(ids).shape)
```

## 練習與解答

輸入 `[2,7,4]` 經 Linear(4,3) 得 `[2,7,3]`；若想句子分類，還要定義 pooling 或選取位置。Conv2d 輸入32×32、K3、P0、S2，輸出高度15。若得到16，重新核對公式的 -1 與 floor，而不是改 Linear 到程式剛好能跑。

## 官方來源與延伸閱讀

- [層與 shape 參考](https://docs.pytorch.org/docs/2.15/nn.html)
