# 神經網路與梯度必要回顧

<figure class="tf-figure"><a href="assets/figures/09-pre-norm-block.svg" target="_blank" rel="noopener"><img src="assets/figures/09-pre-norm-block.svg" alt="輸入X經Norm因果注意力與殘差加法，再經Norm MLP第二次殘差加法，整層保持B S D形狀。" loading="lazy"></a><figcaption>Transformer block的主路徑與殘差。用筆沿主路徑走一次，再分別沿兩條skip走一次，確認每個加法的來源。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>指出模型輸入、機率與決策分別在哪裡，再用本頁算例核對數值或shape。 本頁主題：神經網路與梯度必要回顧。</p></div>

## 模型的參數如何因資料改變

前向計算把輸入和參數變成預測，loss衡量預測與監督目標的差異，梯度指出參數微小變動會怎樣影響loss，最佳化器再決定實際更新。Transformer雖有很多矩陣與路徑，基本學習流程仍是這四步；先把小例子算清楚，比一開始就背大型模型名稱更有用。

梯度不是「正確答案應該是多少」，也不是參數本身的大小。正梯度表示在其他條件不變時，參數往正方向微增會讓loss增加；梯度下降因此往相反方向走。一步更新是否真的降低有限步長的loss，仍受學習率與曲面影響。

## 一個從頭算完的數值例

令模型$\hat y=wx$，$x=2$、真值$y=1$，loss為$L=\frac12(\hat y-y)^2$。初始$w=0$，則預測0、loss0.5。依鏈式法則：

$$
\frac{\partial L}{\partial w}=(wx-y)x=-2
$$

若學習率$\eta =.1$，更新後$w=.2$，預測.4，loss為.18。若$\eta =1$，w變2，預測4，loss反而4.5；方向局部合理不代表任意步長都有效。這個例子同時說明為什麼看到梯度存在，仍要檢查學習率與loss趨勢。

```python
import torch

w = torch.tensor(0., requires_grad=True)
loss = .5 * (2*w - 1)**2
loss.backward()
assert w.grad.item() == -2.
with torch.no_grad():
    w -= .1*w.grad
assert abs(w.item() - .2) < 1e-6
```

這是原創純量反向例，不是完整訓練迴圈；正式迴圈還要處理資料、zero_grad、optimizer與驗證。

## 鏈式法則在多層網路中傳遞

若$a=f(x)$、$b=g(a)$、$L=h(b)$，梯度沿計算圖把局部導數相乘與相加。矩陣情況形狀較多，但原理相同。殘差路徑可提供額外傳遞通道；非線性讓多個線性層不只是等價於一個線性變換。每種操作都要有可定義的反向行為，離散argmax通常不適合放在需要一般梯度的訓練路徑中。

Token IDs本身是離散索引，不會因反向自動變成另一個詞；被更新的是Embedding表中查到的向量與後續參數。對logits先argmax再算普通可微損失，常會切斷你需要的學習訊號，應讓交叉熵直接接logits與整數目標。

## 梯度累積與清零

PyTorch反向通常把新梯度加到`.grad`，不是每次自動覆蓋。若每批都想獨立更新，更新前清零；若刻意做多microbatch梯度累積，就依有效樣本或Token分母安排縮放，再在合適時點更新。忘記清零不是另一種神祕的高效訓練法，而是改變了更新數值。

`optimizer.zero_grad(set_to_none=True)`可以讓未產生梯度的參數保持None；None和數值0在一些最佳化行為與診斷上不同。不要把全部None不經檢查地補成0，掩蓋某條路徑根本沒有參與loss。

## train、eval與no_grad分開看

`model.train()`和`eval()`改變Dropout等模組行為，不等於開啟或關閉參數梯度；`no_grad()`或`inference_mode()`控制梯度追蹤。驗證時通常兩者都需要：eval維持適當層行為，關閉梯度節省計算圖。若只用eval但仍保留每批loss Tensor，可能無意保存很多圖而耗記憶體。

練習：相同純量例連續兩次backward且不清零，w還沒更新，grad是多少？答案−4。若你預期−2，就需要先清零；若是刻意累積兩份資料，也要配合平均分母。再用小有限差分`(L(w+ε)-L(w−ε))/(2ε)`核對梯度，ε過小會受浮點誤差影響，應選合理尺度。

## 官方來源與跨課閱讀

自動微分見[Autograd mechanics](https://docs.pytorch.org/docs/stable/notes/autograd.html)，梯度清零見[Optimizer.zero_grad](https://docs.pytorch.org/docs/stable/generated/torch.optim.Optimizer.zero_grad.html)。更完整張量工程可讀[PyTorch課程](../pytorch/index.html)，本課保留理解Transformer所需的必要回顧，不要求先讀完另一整門才能開始。
