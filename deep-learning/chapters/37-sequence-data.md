# 序列資料：時間、順序、長度與預測位置

先定義能看見哪些位置，再選RNN、CNN或Attention。

## 不是多一個Tensor軸就完成

X[N,T,D]代表batch、位置、每位置特徵，但T可能是時間、字詞或事件順序。分類整段、每位置標註、預測下一步或生成輸出有不同label對齊。先寫預測時能看到哪一段，避免模型偷看答案後面的資訊。

## 時間與樣本的切分

滑動視窗可能大量重疊，隨機切窗可讓train與test共享幾乎相同原始片段。按時間、主體或來源切，再造視窗，必要時留gap。前處理也只fit允許的train期間，不能以未來mean填過去資料。

## 同一模型的不同輸出

many-to-one可用最後有效hidden或mask pooling，many-to-many每步輸出，encoder-decoder另有兩段長度。若拿PAD之後的最後位置作句子表示，可能讓序列長度決定預測；「最後」應是每筆有效序列的最後，而不是矩形Tensor最右邊。

## Shape與batch規則

Torch RNN可batch_first=True使用[N,T,D]，hidden state仍有[num_layers×directions,N,H]形式。LSTM還有cell state；不能看到batch_first就把所有state軸也交換。長度與mask是明確metadata，不應把PAD0當普通token參與平均。

## 本課的生成任務

序列長2..7、ID1..8、PAD0，label為最後token是否>=5。這刻意讓答案可驗證，直接規則是完美基準；GRU專題用來學pack與state，沒有宣稱這個任務需要遞迴。更複雜語意與長期依賴需另外設計資料與評估。

## 練習與解答

預測明天事件，能否用明天已發生後的完整序列？答案：不能，須限定輸入截止時間。對句子分類可看全句，對逐token預測需causal規則，兩者mask不同。先畫時間與label對齊，再寫forward，比之後修一個維度更根本。

## 原始論文與官方來源

- [Sequence models](https://www.deeplearningbook.org/contents/rnn.html)
- [Torch recurrent layers](https://docs.pytorch.org/docs/2.15/nn.html#recurrent-layers)
