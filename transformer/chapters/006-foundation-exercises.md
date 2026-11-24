# 入門練習與解析

<figure class="tf-figure"><a href="assets/figures/02-chain-nll.svg" target="_blank" rel="noopener"><img src="assets/figures/02-chain-nll.svg" alt="BOS我想睡四格序列下有三個條件機率0.5,0.25,0.8，相乘0.1，負對數相加2.3026，三token平均0.7675。" loading="lazy"></a><figcaption>條件機率鏈與負對數似然。平均損失的分母是有效預測目標，不是字數、句數或輸入格數。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>指出模型輸入、機率與決策分別在哪裡，再用本頁算例核對數值或shape。 本頁主題：入門練習與解析。</p></div>

## 題目一：把整段機率與平均loss分開

一段文字有三個有效預測位置，模型對真實Token的機率依序.5、.5、.25。請算整段條件機率、總NLL與平均NLL，使用自然對數。

**解析：**整段機率=.0625，總NLL=`−ln(.0625)≈2.7726`，平均NLL≈.9242。若多補兩個padding位置，它們不應增加有效預測數，所以平均分母仍3。把分母改成5會讓loss虛降，但模型並沒有學得更好。

延伸：PPL為`exp(.9242)≈2.5198`。不能把這個數直接拿去和另一份Tokenizer的PPL比較，因為Token單位可能不同；比較資料、條件與有效mask也需固定。

## 題目二：模型輸出究竟有幾個分數

B=2、$T=5$、$D=12$、V=30，Embedding輸出和語言模型logits分別什麼shape？下一步生成通常取哪一部分？

**解析：**Embedding為`[2,5,12]`，logits為`[2,5,30]`。若兩段都沒有尾端padding且最後位置就是有效上下文末端，可取`logits[:, -1, :]`得到`[2,30]`作下一步候選。若批次含不同長度右padding，不能一律取最後欄；需依每段有效末端處理，或採與模型相容的生成批次政策。

D是內部表示寬度，V是候選Token數，兩者不能交換。雖然有些玩具例剛好$D=V$，仍應用不相同維度測試，避免錯誤軸被巧合掩蓋。

## 題目三：能相乘就代表算對嗎

Q的shape為`[2,3,5]`，K為`[2,4,5]`。若要每個query比較四個key，分數shape應是什麼？

**解析：**`Q @ K.transpose(-2,-1)`得到`[2,3,4]`。最後兩軸分別是query位置與key位置。若程式把B與T攤平後讓不同序列互相比較，矩陣可能仍相容，但語意已錯。要用批次隔離測試：修改第二段的Token，不應改變第一段的有效輸出。

延伸：padding mask原為`[B,T_k]`，配多頭分數`[B,H,T_q,T_k]`時可明確擴成`[B,1,1,T_k]`，讓所有頭與query共享同一份key有效性。不要只憑維度相同讓廣播自動猜測。

## 題目四：一個參數的兩種學習率

模型$\hat y=wx$，$x=2$、$y=1$、$w=0$、平方loss含1/2。梯度是多少？$\eta =.1$與$\eta =1$更新後的loss各是多少？

**解析：**梯度−2。$\eta =.1$後$w=.2$、loss=.18；$\eta =1$後$w=2$、loss=4.5。較大學習率並非必定更快學會；更新太遠可能跨過低點。若連續兩次backward未清零，更新前grad會變−4，這又是另一份更新契約，不可和單次結果混報。

## 題目五：環境與模式造成的差異

兩位同學載入相同權重與輸入，一位用train，一位用eval，Dropout開啟時結果不同，是否能直接判定儲存壞掉？

**解析：**先確認模型模式、隨機種子、版本與前處理。train模式的Dropout會引入隨機遮蔽，eval則關閉該行為；但eval不會自動關閉Autograd。要做固定推論，通常配合eval與inference_mode，並檢查資料與權重雜湊。只有在條件一致後仍有超出容忍的差異，才進一步查實作或檔案。

## 可交付的基礎驗收

請交一份三欄表：假設、預期shape／數值、實際結果。至少包含一個機率乘積、一個有效Token分母、一個非巧合維度的矩陣乘法、一個有限差分梯度與一個模式切換例。對每個失敗案例先寫「哪個假設不成立」，再改程式；不要只改到錯誤訊息消失。

這些題目是後面Attention、packing與訓練的共同基礎。你能用少量可核對資料找出錯誤，再放大到較複雜模型，才不會只依賴loss曲線猜測。原始規則可回查[PyTorch matmul](https://docs.pytorch.org/docs/stable/generated/torch.matmul.html)、[CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)與[Autograd](https://docs.pytorch.org/docs/stable/notes/autograd.html)。
