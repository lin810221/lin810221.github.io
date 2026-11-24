# 向量矩陣與批次形狀

<figure class="tf-figure"><a href="assets/figures/31-tensor-complexity-map.svg" target="_blank" rel="noopener"><img src="assets/figures/31-tensor-complexity-map.svg" alt="五列表格將token hidden QKV dense scores cache對應形狀，dense scores平方長度，cache線性長度再乘dtypebytes。" loading="lazy"></a><figcaption>張量形狀、密集注意力與cache對照。估算時先確認物件：注意力工作矩陣、歷史KV與模型權重不是同一筆記憶體。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>指出模型輸入、機率與決策分別在哪裡，再用本頁算例核對數值或shape。 本頁主題：向量矩陣與批次形狀。</p></div>

## 形狀是計算契約，不只是報錯訊息

本課固定B代表batch數、T代表序列長度、D代表模型寬度、V代表詞彙大小、H代表Attention頭數、d_h代表每頭寬度。輸入Token IDs是`[B,T]`，查表後是`[B,T,D]`，語言模型頭輸出`[B,T,V]`。這些符號同時交代每個軸的意義，不能只記一串數字。

例如B=2、$T=4$、$D=6$，表示兩段序列，各四個位置，每位置六維表示。`[2,4,6]`不是八段獨立句子，也不是每個Token只有六種可能答案；可能答案數由V決定。將T和D互換可能仍能進行某些矩陣乘法，卻改變了模型在混合什麼資訊。

## 線性投影作用在最後一軸

數學上以列向量慣例寫$Y=XW$，若X是`[B,T,D]`、W是`[D,F]`，結果是`[B,T,F]`。PyTorch的`nn.Linear(D,F)`將權重儲成`[F,D]`並在內部使用轉置，因此讀取實際weight.shape時不要以為教材矩陣寫反。

```python
import torch

x = torch.arange(2*4*6, dtype=torch.float32).reshape(2, 4, 6)
w = torch.ones(6, 8)
y = x @ w
assert y.shape == (2, 4, 8)
assert torch.allclose(y[0, 0], torch.full((8,), 15.))
```

第一個位置向量是0到5，總和15；W每欄都是1，所以八個輸出皆15。這是原創形狀算例，實際可學投影的各欄不會都相同。

## Attention在哪兩個軸做兩兩比較

單頭Q和K分別是`[B,T_q,d_h]`、`[B,T_k,d_h]`。計算`Q @ K.transpose(-2,-1)`得到`[B,T_q,T_k]`，每列是一個query對所有key的分數。再乘V張量`[B,T_k,d_v]`，得到`[B,T_q,d_v]`。T_q與T_k可以不同，這是CrossAttention與cache時的重要線索。

若忘記轉置最後兩軸，可能shape直接不相容；若剛好$T=d_h$，乘法可能意外合法，卻算錯了軸。因此測試最好使用不相等的維度，例如$T=3$、d_h=5，讓錯誤不容易被巧合掩蓋。

## 廣播可以幫忙，也會隱藏錯誤

位置表`[T,D]`加到`[B,T,D]`時，沿batch共享是合理廣播。padding mask若是`[B,T_k]`，加到多頭分數`[B,H,T_q,T_k]`前，通常要明確變成`[B,1,1,T_k]`。若未加軸，可能直接報錯，也可能在某些相同尺寸下對錯誤軸對齊，形成難查的語意錯誤。

一個安全方法是先寫每個中間Tensor的軸名與shape，再使用`assert`驗證。數值能算完不是充分條件；你還要測「修改某段序列的padding內容，不影響另一段有效結果」等不變性，證明軸真的對應正確資料。

## reshape、transpose與記憶體排列

多頭通常先把`[B,T,D]`拆成`[B,T,H,d_h]`，再轉成`[B,H,T,d_h]`。這不是把Token重新排序成新句子，而是將每個位置的通道分配到不同頭。轉置後的Tensor可能不連續；`view`有時不適用，可依需要使用`reshape`或先`contiguous()`，但都要確認語意與可能的記憶體複製。

練習：$D=12$、$H=3$時d_h是多少？答案4。若$D=10$、$H=3$，標準等寬拆頭不成立，不能用整數除法偷偷丟掉一維；要拒絕設定或採另一個明確架構。再問：`[B,H,T,d_h]`直接reshape成`[B,T,D]`是否總正確？不，先將H與T軸轉回原順序，再合併頭維度。

## 來源與驗收

廣播規則見[PyTorch broadcasting semantics](https://docs.pytorch.org/docs/stable/notes/broadcasting.html)，線性層權重見[Linear](https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html)，形狀操作見[Tensor.reshape](https://docs.pytorch.org/docs/stable/generated/torch.Tensor.reshape.html)。交付一張軸名表，至少使用兩組非巧合尺寸測試，不只在$T=D$的單一例子上確認程式能跑。
