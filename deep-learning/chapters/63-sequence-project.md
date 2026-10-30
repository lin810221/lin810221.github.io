# 專題三：變長序列、最後token與有效長度

把padding、packed sequence與任務規則連成可測試的序列分類流程。

## 任務與一個很強的baseline

240筆序列，長度2至7，token為1至8，標籤為最後有效token是否至少5。切成144／48／48。直接讀最後有效token就能100%符合生成規則，所以GRU在此是流程教學，不是比規則更好的方法。當你知道真實問題有這種可靠規則，通常應先使用規則。

## 批次不等於同樣長度

collate將一批補到其中最大長度，PAD保留為0，長度另以CPU long tensor保存。Embedding有9個ID、維度8、padding_idx=0；GRU hidden12，最後hidden接Linear2。pack_padded_sequence會依有效長度排除尾端padding，enforce_sorted=False允許批次未預先排序。此例全為非空序列，不能用長度0偷渡。

## 為何不是拿最後一欄

對不同長度直接用output[:,-1]，短序列可能讀到padding後狀態。即使PAD embedding為零，RNN還有偏置與recurrent轉換，走過一個零向量仍可能改hidden。可以用正確length索引最後有效輸出，或如本例採packed sequence並取對應最後hidden。雙向或多層網路還要另外理解hidden的層／方向維度。

## 驗證不變性

先用相同有效token但不同額外尾端padding，比較預測，長度都保持原有效值。再只改早期token，檢查模型是否近似遵守最後token規則；這不是任何參數都保證成立，但可作為學習行為的測試。最後改最後token，確認標籤與預測能跟著變。資料生成規則提供我們清楚的期望。

## 從本課走向真實序列

真實資料需先決定序列邊界、時間順序、同一個體是否跨split，以及缺值與事件間隔如何編碼。文本還有tokenizer、詞彙外與截斷政策。不可因本例使用Embedding就視為已經完成自然語言理解；任務資訊和表示仍非常簡化。

## 練習與解答

長度為[2,4]、張量寬度4，第一筆最後有效索引是多少？答案：1，因索引從0開始。若所有padding都設attention mask，能否取代GRU的pack？不能；GRU沒有自動讀Attention mask參數，必須使用其支援的長度處理或手動選取有效狀態。

## 原始論文與官方來源

- [Packed sequence](https://docs.pytorch.org/docs/2.15/generated/torch.nn.utils.rnn.pack_padded_sequence.html)
- [GRU輸入與hidden](https://docs.pytorch.org/docs/2.15/generated/torch.nn.GRU.html)
