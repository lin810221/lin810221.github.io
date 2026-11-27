# 條件機率對數與資訊量

<figure class="tf-figure"><a href="assets/figures/02-chain-nll.svg" target="_blank" rel="noopener"><img src="assets/figures/02-chain-nll.svg" alt="BOS我想睡四格序列下有三個條件機率0.5,0.25,0.8，相乘0.1，負對數相加2.3026，三token平均0.7675。" loading="lazy"></a><figcaption>條件機率鏈與負對數似然。平均損失的分母是有效預測目標，不是字數、句數或輸入格數。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>指出模型輸入、機率與決策分別在哪裡，再用本頁算例核對數值或shape。 本頁主題：條件機率對數與資訊量。</p></div>

## 你需要的機率工具其實很集中

語言模型在每個上下文後給出一個候選分布，所有候選機率非負且總和1。條件機率$p(y\mid x)$表示已知x時，y的機率；不能把它和$p(x\mid y)$交換。某個詞後常接另一個詞，不表示反向也同樣常見，序列方向是模型問題的一部分。

假設玩具語料有10次「天氣」上下文，其中6次接「好」、3次接「壞」、1次接EOS，經驗條件比例是.6、.3、.1。這只是該小樣本的統計，不是世界上所有句子的真實分布；神經網路則試圖在大量不同上下文間共享參數，不能單純把每個完整上下文都當獨立查表。

## 為什麼要取對數

連續很多機率相乘很容易變得極小，對數把乘積轉成加總，也讓訓練更方便。若三步正確機率是.5、.25、.8，整段機率.1，負自然對數是約2.3026；也等於`−ln(.5)−ln(.25)−ln(.8)`。使用哪個對數底數要寫明：本課loss以自然對數為主，單位常稱nats；以2為底則是bits。

$$
-\log \prod_t p(x_t\mid x_{<t})
=-\sum_t\log p(x_t\mid x_{<t})
$$

不要直接對logits取log。logits可能為負，且未正規化；應使用log_softmax或數值穩定的交叉熵。真實機率若趨近0，負對數懲罰會很大，這使高信心錯誤在目標函式中代價明顯。

## 交叉熵與一個已知正確Token

若真實下一個Token是類1，模型給它機率.25，這個位置的NLL是`−ln(.25)≈1.3863`。one-hot真值的交叉熵只選出正確類的負對數；它不是對所有候選機率取平均，也不是「最高分猜對就 $\mathrm{loss}=0$ 」。只要正確類機率還沒到1，loss通常仍為正。

模型在同樣的真值上給正確類.6與.9時，即使兩次argmax都對，NLL分別約.5108與.1054。這顯示分類命中率與分布品質可以不同；但降低語料loss仍不等於所有回答都事實正確或對所有任務都安全可靠。

## 平均分母與perplexity

令M為有效預測Token數，平均NLL是總NLL除M。Perplexity定義為平均NLL取指數：

$$
\operatorname{PPL}=\exp\left(\frac{1}{M}\sum_{i=1}^{M}-\log p(y_i\mid c_i)\right)
$$

若兩個有效位置的正確機率為.5與.25，平均NLL約1.0397，PPL約2.8284。這不是模型每一步都恰好在2.8284個詞間平均選擇，而是幾何平均意義的摘要。若padding位置不該預測，不能把它們算進M；若mask不同，兩個loss就不是相同分母。

## 不同Tokenizer的PPL不可直接排名

同一段文字可被不同Tokenizer切成不同數量與單位的Token。把字元級PPL、byte級PPL與另一份子詞詞彙表PPL直接並排，會混入單位差異。至少固定模型對應Tokenizer、資料、起始條件、有效位置與截斷政策；跨Token單位比較需選合適的標準化量並說明編碼。

同樣地，整段機率通常隨長度下降，不應拿長句與短句的原始乘積判定哪段較自然。平均每Token也仍受Tokenizer與長度分布影響，不是一個脫離資料條件的絕對智力分數。

## 練習與解析

四個位置的NLL為`[1,2,0,0]`，最後兩個是padding且應忽略。正確平均是多少？答案1.5，不是0.75；後兩個零是未參與，不是模型完美預測的兩個Token。PPL應為`exp(1.5)≈4.4817`。

若把自然對數loss直接餵給`2**loss`，會得到另一個錯誤數字。先把對數底數與還原函數配對，再檢查分母。API可查[log_softmax](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.log_softmax.html)與[CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)；本單元數值為原創機率算例。
