# Pooling與下採樣：資訊、等變性與aliasing

分清最大、平均、stride與global pooling對模型造成的偏好。

## 為什麼降低解析度

下採樣減少activation與運算，後面每個位置可間接看更大原始區域。但也丟資訊，細小物體、邊界或位置任務可能受影響。不能只看模型變小，就說表示更好；要連回任務與資料。

## Max與Average

max pooling偏向局部最強反應，平均則保留區域平均。max的gradient傳到選中位置，tie有API約定；平均分配到各項。它們通常無可學參數，但會改梯度、解析度與不變性。stride convolution則包含可學權重，兩者不完全可替代。

```python
import torch
from torch.nn import functional as F
x=torch.tensor([[[[1.,2.],[3.,4.]]]],requires_grad=True)
out=F.max_pool2d(x,2)
out.sum().backward()
print(out,x.grad)
print(F.avg_pool2d(x.detach(),2))
```

max為4，只有右下得到此處gradient1；average為2.5。這個局部例子可幫你解釋下採樣的不同訊號。

## 平移與aliasing

stride取樣可能對一像素移動敏感，因為取到的格點不同；下採樣前低通等策略可研究，但也有資料與性能取捨。CNN的共享不保證任意平移後最後分類完全不變，更不保證旋轉與尺度不變。

## Global Average Pooling

將每channel空間平均，可減少固定Flatten的尺寸相依與全連接參數，但丟掉精確位置。對分類有時合適，對定位／序列位置重要時未必。本課TinyCNN保留小型Flatten以便直接核對128個特徵，不把某個設計當唯一方案。

## 練習與解答

物體只占一個亮點，max與average可能有不同反應；若亮點是noise，max也可能放大錯訊號。解答：沒有一個pooling永遠最好，使用合理資料與驗證，檢查小物體／位置切片。更完整偵測與分割架構將在獨立影像課深入。

## 原始論文與官方來源

- [Pooling layers](https://docs.pytorch.org/docs/2.15/nn.html#pooling-layers)
- [CNN結構](https://www.deeplearningbook.org/contents/convnets.html)
