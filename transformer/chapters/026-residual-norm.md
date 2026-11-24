# 殘差LayerNorm與PreNorm

<figure class="tf-figure"><a href="assets/figures/09-pre-norm-block.svg" target="_blank" rel="noopener"><img src="assets/figures/09-pre-norm-block.svg" alt="輸入X經Norm因果注意力與殘差加法，再經Norm MLP第二次殘差加法，整層保持B S D形狀。" loading="lazy"></a><figcaption>Transformer block的主路徑與殘差。用筆沿主路徑走一次，再分別沿兩條skip走一次，確認每個加法的來源。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>沿殘差與主路徑追蹤shape，區分逐Token運算與跨Token混合，並核對本頁的參數或正規化。 本頁主題：殘差LayerNorm與PreNorm。</p></div>

## 殘差讓區塊學習加上什麼

殘差將輸入x與子模組輸出F(x)相加，得到x+F(x)。兩支shape必須相容，通常都為`[B,T,D]`。它提供一條保留原表示的路徑，也讓梯度有直接傳遞項；不表示F一定很小、不表示層數可無限制增加，也不保證所有訓練設定都穩定。

原創向量例子：x=`[1,2]`、F(x)=`[.1,-.2]`，相加為`[1.1,1.8]`。若F輸出`[B,T,F]`而F不等於D，不能靠殘差自動補齊；需先投影回D。一般Transformer的FFN第二層與Attention輸出投影都負責恢復可相加形狀。

## LayerNorm在每個位置內計算

對本課`[B,T,D]`，LayerNorm(D)通常沿最後D維求均值與變異數，再使用可學gamma與beta。它不把不同batch或不同Token混在一起求統計，與BatchNorm的典型用途不同。PyTorch LayerNorm採其定義的母體式變異數，不應用不相同的unbiased樣本變異數手算後判定框架錯誤。

$$
\operatorname{LN}(x)_i=\gamma_i\frac{x_i-\mu}{\sqrt{\sigma^2+\epsilon}}+\beta_i
$$

x=`[1,3]`，均值2、母體變異數1；若gamma=1、beta=0，忽略極小ε時得到`[-1,1]`。x加同一常數5成`[6,8]`，中心化結果相同。若每個維度加不同數，則不具這個簡單不變性。

## PreNorm與PostNorm先後不同

一個PreNorm子層可寫`x + F(LN(x))`；PostNorm則是`LN(x + F(x))`。兩者不是只改程式排版：正規化作用在不同路徑，梯度與訊號尺度也不同。標準區塊通常有Attention與FFN兩個子層，各有自己的Norm與殘差，不能把兩者共用一次Norm就當成相同設計。

[Layer Normalization原始論文](https://arxiv.org/abs/1607.06450)提供正規化背景；[Xiong等人研究](https://arxiv.org/abs/2002.04745)討論Transformer中Norm位置與訓練行為。研究結果有其模型與假設，不應把PreNorm寫成所有任務、深度與最佳化條件下無條件最佳。

## 最終Norm與Dropout也要算進圖

PreNorm堆疊後常另加final Norm再接語言模型頭，具體以模型config為準。若手寫模型漏掉這一步，載入同shape外部權重仍可能不等價。Dropout可放在子層輸出後、殘差相加前等位置，順序與模式要固定；不能只寫「有Dropout」卻不交代作用在哪裡。

LayerNorm本身通常在train與eval使用相同當下輸入統計，不維護BatchNorm式running mean；但包住它的區塊有Dropout時，整體輸出仍會因模式不同而變。把這兩件事分開，才能正確診斷eval差異。

## 數值穩定與錯誤診斷

ε避免零變異數除零，也會影響極小尺度下的不變性。不同dtype與預設eps不一定相同，對照時明確指定。所有維度都相同的向量，中心化後為0，輸出主要由beta決定；這不是模型一定壞掉，而是Norm定義的結果。

練習：把整個batch多加一段完全不同序列，原序列的單獨LayerNorm結果應改變嗎？不應，因統計沿每個位置D維；若改變，查是否誤沿batch或時間軸正規化。再問：`LN(x)+F(x)`是否等於PreNorm？不等，PreNorm是`x+F(LN(x))`，輸入殘差本身保留x。

## 驗收與官方介面

保存區塊運算順序、Norm軸、eps、gamma/beta、final Norm與Dropout位置。用極小向量核對均值與變異數，再測batch隔離與梯度有限。官方定義見[PyTorch LayerNorm](https://docs.pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html)，不要只用輸出shape判定PreNorm／PostNorm相容。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 09_norm_ffn.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:09_norm_ffn.py -->

