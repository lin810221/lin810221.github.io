# 正弦位置編碼

<figure class="tf-figure"><a href="assets/figures/06-rope-relative-angles.svg" target="_blank" rel="noopener"><img src="assets/figures/06-rope-relative-angles.svg" alt="兩張圓圖中Q60度K20度與Q90度K50度有相同40度角差，說明共同位移不改變相對旋轉。" loading="lazy"></a><figcaption>RoPE：旋轉如何帶入相對位置。先理解相對角差，再區分頻率、position_id、長度外推與模型實際可用範圍。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>找出查表、維度或位置的作用，說明它如何改變本頁的輸入表示與輸出分數。 本頁主題：正弦位置編碼。</p></div>

## 用固定函式產生位置向量

正弦位置編碼不為每個位置各學一列，而是以不同頻率的sin與cos產生D維向量。經典做法把相鄰兩維視為同頻率的一組，並將位置向量加到Token表示。固定函式減少位置表參數，也讓未列在訓練表裡的位置有可計算數值，但這不自動保證模型在更長序列上表現可靠。

這個設計的歷史來源是[Attention Is All You Need](https://arxiv.org/abs/1706.03762)。下面以原創小尺寸推導，重點是理解頻率、shape與數值；具體模型可能使用不同base、縮放或完全不同的位置方法，不應把此式套成所有Transformer的必要格式。

## 公式中每個符號是什麼

令p為位置、D為偶數模型寬度、i從0到D/2−1。本單元採base=10000的經典形式：

$$
PE(p,2i)=\sin\left(p/10000^{2i/D}\right),\qquad
PE(p,2i+1)=\cos\left(p/10000^{2i/D}\right)
$$

同一組兩維使用相同角度，但一個sin、一個cos。i較大時頻率較低，隨位置變化較慢；多組頻率共同描述位置，不是每個維度各自代表「第幾個詞」。位置0的sin部分為0、cos部分為1，因此整個向量不會全部是0。

## $D=4$的手算例

$D=4$時，第一組角度為p，第二組為p/100。位置0向量`[0,1,0,1]`；位置1約為`[.84147,.54030,.01000,.99995]`。若把第二組分母誤算成10000，說明你漏掉指數2i/D；如果把sin與cos全部取相同位置，則沒有建立成對頻率。

```python
import math

def pe4(position):
    return [math.sin(position), math.cos(position),
            math.sin(position/100), math.cos(position/100)]

assert pe4(0) == [0., 1., 0., 1.]
assert abs(sum(v*v for v in pe4(7)) - 2.) < 1e-12
```

每組sin²+cos²=1，所以這個4維向量的平方範數為2；它是檢查頻率配對的簡單不變量。若後面加入縮放或其他處理，則要相應調整預期，而不是拿此值檢查完全不同模型。

## 相對位移如何出現在內積

同頻率兩組位置向量的內積包含$\sin(a)\sin(b)+\cos(a)\cos(b)=\cos(a-b)$。因此固定頻率對位置差有可描述的結構。這有助理解為何成對三角函式有用；但實際輸入是內容加位置，經Q/K投影後還有內容交互項，不能直接說最終Attention分數只由距離決定。

若只看單一sin維度，它有週期且可能在不同位置取相同值；多頻率向量一起使用較能區分範圍內位置，但有限浮點精度與實際長度都要考慮。不要把「可以算公式」寫成數學上對所有整數位置永不混淆且永遠可用的模型保證。

## 工程上的位置、型別與padding

位置編碼可預先算成buffer，也可按需建立。它通常不是可學Parameter，但仍需隨模型移到正確device與dtype；在CPU建表卻忘記搬到GPU，會出裝置不一致錯誤。低精度大位置的三角函式計算也需注意精度，常用較高精度計算再轉型。

padding方向與position_ids仍需依序列邏輯處理，固定函式不會自動知道哪個欄位是假位置。輸入寬度若為奇數，要明確定義最後一維怎麼處理；本課基礎推導採偶數D，不能讓程式默默少一欄再期待廣播解決。

## 練習與解析

$D=4$時，位置2的第一組角度是2，第二組是.02；不是每一維都用位置2除同一個10000。請核對兩組平方和各為1，再把位置差3的兩個同頻率向量內積和cos(3ω)比較。

如果模型只訓練到長度32，現在公式能算到320，能否直接宣稱上下文已擴展十倍？不能。仍需長度外推評估、記憶體與遮罩／cache一致性驗收。數值介面可查[torch.sin](https://docs.pytorch.org/docs/stable/generated/torch.sin.html)與[torch.cos](https://docs.pytorch.org/docs/stable/generated/torch.cos.html)，真實模型能力由獨立資料驗證。
