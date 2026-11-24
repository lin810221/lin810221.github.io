# 縮放點積與Softmax

<figure class="tf-figure"><a href="assets/figures/07-qkv-numerical.svg" target="_blank" rel="noopener"><img src="assets/figures/07-qkv-numerical.svg" alt="查詢1和兩個key1,0得到分數1,0，softmax為0.7311,0.2689，再用此顯示權重加權V兩列2,0與0,4得到1.4622,1.0756。" loading="lazy"></a><figcaption>Q、K、V：先找關聯，再聚合內容。自己改一個V值，確認權重不變而輸出改變；再改K值觀察權重。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>依Q、K、V與遮罩逐步計算；核對每列權重分母、head軸和可見位置。 本頁主題：縮放點積與Softmax。</p></div>

## 四步組成一個Attention

先用QK內積得到位置配對分數，除以每頭Key寬度平方根，再加入可見性限制，沿key軸softmax，最後乘Value。單頭常寫：

$$
\operatorname{Attention}(Q,K,V)=
\operatorname{softmax}\left(\frac{QK^\top}{\sqrt{d_h}}+M\right)V
$$

M在允許處為0、不允許處為負無限大；這是加性mask記法，不是所有API的布林語意。softmax的dim應是key位置，因為每個query要在它可讀的來源之間分配權重。若沿query軸正規化，shape可能不變，但計算意義錯了。

## 為什麼除以平方根

在簡化假設下，若q、k各維近似獨立、均值0、變異數1，d_h項乘積相加的變異數約隨d_h增加。除以sqrt(d_h)讓分數尺度較穩，避免維度變大時softmax過度尖銳。這是設計動機，不是所有訓練後Q/K都嚴格符合獨立標準分布的宣告。

縮放用的是Q/K內積維度，不是序列長度T，也不一定是整體模型寬度D。標準等寬多頭$D=32$、$H=4$時，d_h=8，預設縮放是1/sqrt(8)。若錯除sqrt(32)，會改變分布溫度，不是無關緊要的記法差異。

## 一個兩key的手算

假設QK未縮放分數是`[2,0]`，d_h=4，縮放後`[1,0]`，softmax約`[.73106,.26894]`。Values是兩個純量10與2，輸出約`7.84847`。若忘記縮放，權重約`[.88080,.11920]`，輸出約`9.04638`；兩個結果都可計算，但代表不同Attention設定。

若只允許第一個key，第二個分數設為−∞，權重變`[1,0]`，輸出10。不能把禁止分數設0取代−∞，因為0仍是可參與softmax的普通分數；當合法分數為負時，禁止位置甚至可能得到更高權重。

## 穩定softmax與全遮罩列

對logits`[1000,1001]`直接exp可能溢位。減去最大值變`[-1,0]`，softmax不變，卻較穩定。可用框架提供的softmax／log_softmax，不需自行在不合適精度下重寫；參考實作則應清楚展示數值政策。

若某一query所有key都是−∞，減最大值會出現未定形式，普通softmax可能得到NaN。有效query應至少有一個合法key；無效padding query要採明確排除或安全處理。不要用一個大負數掩蓋此問題：全是相同有限負數時，softmax可能變均勻分布，反而讓本應不可見的位置都被讀取。

## 權重與輸出各有可測不變量

沒有Dropout時，合法列的權重非負、和為1，不允許位置權重為0。若Value是純量，輸出在允許Values的最小與最大之間；若所有Values相同，輸出也相同。開啟Attention Dropout後，隨機遮蔽與縮放可能讓單次權重和不再剛好1，檢查應先固定dropout=0。

權重越尖銳不代表模型一定更懂；可能只是Q/K尺度變大。比較不同設定時，同時看loss、任務結果與數值穩定，而不是用熱圖顏色深淺當品質分數。

## 練習與解析

一個query對兩個key分數相同，Values為`[2,6]`，無mask、無dropout，輸出多少？權重各.5，輸出4。若只允許第二個key，輸出6；若兩個都禁止，應按無合法來源政策報錯或排除，不能偷偷回4。

再問：把每列分數都加上100，權重是否改變？不變；但把分數乘100通常會變尖銳。相加與乘法的影響不同，這是檢查穩定softmax與溫度設定的好題。原始公式見[Transformer論文](https://arxiv.org/abs/1706.03762)，實作介面見[PyTorch 2.15 SDPA](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 06_attention_arithmetic.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:06_attention_arithmetic.py -->

