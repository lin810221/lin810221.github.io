# 必要數學推導與手算

<figure class="tf-figure"><a href="assets/figures/31-tensor-complexity-map.svg" target="_blank" rel="noopener"><img src="assets/figures/31-tensor-complexity-map.svg" alt="五列表格將token hidden QKV dense scores cache對應形狀，dense scores平方長度，cache線性長度再乘dtypebytes。" loading="lazy"></a><figcaption>張量形狀、密集注意力與cache對照。估算時先確認物件：注意力工作矩陣、歷史KV與模型權重不是同一筆記憶體。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>選本頁一個概念對照圖中shape、公式或除錯分支，說出下一個需要核對的條件。 本頁主題：必要數學推導與手算。</p></div>

## 先固定向量和矩陣的方向

本課將一批序列的隱狀態寫成$B\times T\times D$。單個head內，query矩陣為$T_q\times d_h$，key為$T_k\times d_h$，因此$QK^\top$是$T_q\times T_k$。每列對應一個query、每欄對應一個key；softmax沿key軸計算，再乘$V$得到每個query的內容聚合。

這個方向比記住一串函式名稱更有用。若把softmax沿query軸計算，張量形狀可能仍能相乘，但得到的不是原本定義的注意力。手算時在矩陣旁寫出軸名，程式中也用小型不對稱長度，例如2個queries、3個keys，較容易暴露轉置錯誤。

## Softmax與穩定計算

對logits $z_j$，$p_j=\exp(z_j)/\sum_k\exp(z_k)$。同時減去任意常數不改變分布，因此可取最大值$m=\max_j z_j$，使用$\exp(z_j-m)$避免巨大正數指數溢位。這不是近似技巧，而是代數上相同的比值，實際結果仍有浮點四捨五入。

原創二類例令$z=[\ln3,0]$，指數為$[3,1]$，機率是$[0.75,0.25]$。兩個分數都加100，理論機率不變；直接對很大的數取exp卻可能造成數值問題。取樣temperature則是除以正數$T$，會改變相對差距，因此不是同樣的平移不變性。

## Cross entropy為何得到p減y

若真實類別是第1類，單token負對數似然為$\ell=-\log p_1=\log4\approx1.3863$。把softmax代入，可寫成：

$$
\ell=-z_y+\log\sum_j\exp z_j,\qquad
\frac{\partial\ell}{\partial z_j}=p_j-\mathbf{1}[j=y].
$$

因此上例的logit梯度為$[0.75,-0.75]$。梯度下降減去這個向量，會壓低錯誤第0類的相對分數、提高真實第1類；它不是直接把機率強制設成0和1。若loss是$n$個有效token的平均，每個token對總梯度的貢獻還要除以$n$，PAD忽略位置不應進入分母。

數值穩定的寫法可用$-z_y+m+\log\sum_j\exp(z_j-m)$，實作通常交給框架的cross entropy／logsumexp。不要先softmax，再把機率交給要求logits的CrossEntropyLoss，否則計算的目標已改變。

## Attention是一個加權和

取一維query $q=1$，兩個keys為1和0，縮放因子$\sqrt{d_h}=1$，分數得到$[1,0]$。完整精度權重約為$[0.7310586,0.2689414]$。若兩個value列為$[2,0]$與$[0,4]$，輸出約$[1.462117,1.075766]$。圖解若先把權重取四位小數再乘，會得到略有差異的數字；比較程式時不要用已四捨五入的圖解要求逐位相同。

此輸出是兩個value的混合，不是選出較大權重那一列。改V只會改聚合內容，固定Q/K時權重不變；改K則可能改權重。mask在softmax前排除不允許的位置，不能用score乘0代替，因為$\exp(0)=1$仍有機率。

## Norm與RoPE保留了什麼

對單個token的特徵$[1,3]$，平均為2，母體式變異數為1。暫時忽略epsilon、取gamma=1與beta=0，LayerNorm得到$[-1,1]$。實際程式保留正epsilon並學習仿射參數；統計軸是特徵，不是把不同句子的token混成同一個平均。Norm的目的是調整表示尺度，不會自動修復標籤或因果mask。

RoPE可用二維旋轉矩陣$R_m$理解。令$q'=R_mq$、$k'=R_nk$，則：

$$
(q')^\top k'=q^\top R_m^\top R_nk=q^\top R_{n-m}k.
$$

正交旋轉保留向量長度，內積同時帶入位置差。多維實作對不同維度對採不同頻率，維度配對慣例要與權重相符。這個式子說明位置機制，不保證任意長度外推都維持語言能力。

## 序列損失與Perplexity

若三個目標的條件機率為0.5、0.25、0.8，序列機率0.1，總NLL為$-\ln0.1\approx2.302585$；平均NLL為0.767528，PPL約2.154435。BOS是這個案例的前綴條件，不額外增加一個目標分母。若有EOS目標，它就應依資料規則納入，不能因為它不是一般文字就任意刪掉。

## 練習與解析

**題目：** 把所有logits加10，softmax是否改變？改成全部乘2呢？若PAD score乘0，是否已經遮蔽？

**解析：** 同加常數不改理論機率；乘2放大相對差，通常使分布更集中，只有特殊相同分數情況不變。PAD score設0仍會取得softmax質量，應使用明確bool或additive負無窮遮罩。這三個操作有不同的代數效果，不能因為數值看起來變小就視為等價。

## 參考與日期

查核日期：2026-11-24，數值與推導組合為原創。

- [Transformer原始公式](https://arxiv.org/abs/1706.03762)
- [CrossEntropyLoss官方定義](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html)
- [RoFormer／RoPE原始研究](https://arxiv.org/abs/2104.09864)
