## 一句話不會直接變成一個數字

文字通常先經 tokenizer 變成 token IDs。token 可能是詞、子詞或字節片段，並非固定一個中文字或英文單字。ID 是詞彙表中的索引，不表示語意距離：ID 相差 1 不代表意義接近。

Embedding table 是可學習矩陣，依 token ID 取出初始向量。上下文模型再讓每個位置根據整段輸入產生 hidden state。最後若任務需要單一固定長度向量，還要使用適合的 pooling 或模型設計。

## 四個不同物件

| 物件 | 形狀示意 | 含義 |
| --- | --- | --- |
| Token IDs | `[batch, tokens]` | 詞彙索引 |
| Embedding table | `[vocabulary, hidden_dim]` | 初始查表參數 |
| Token hidden states | `[batch, tokens, hidden_dim]` | 帶上下文的位置表示 |
| Sentence vectors | `[batch, output_dim]` | 給下游任務使用的整段表示 |

hidden_dim 與最後 output_dim 可以不同。模型可能另外投影、正規化或採特定 token 表示。不要只看 backbone 名稱就推論它的輸出契約。

## 同一詞在不同句子

英文 bank 在銀行與河岸語境可以有不同 contextual hidden states；初始查表向量可能相同，但後面的表示受上下文影響。BERT 是理解雙向上下文表示的重要入口。[BERT 原論文](https://arxiv.org/abs/1810.04805)

不過 contextual 不等於對所有句子語意任務都適合。從一般語言模型任意取一層平均，可能需要額外訓練與評估，不能只因它是大模型就把向量品質視為已知。

## Padding 與特殊 token

不同長度句子組成 batch 時常加入 PAD。mask 決定哪些位置是真正輸入。mean pooling 需處理 PAD，是否包含 CLS、SEP 等特殊 token 則依模型 recipe，不宜一概刪除。

如果把 PAD 的 hidden states 混入平均，可能改變向量長度與方向。即使 PAD 恰好為零，只改變平均尺度，後續若未正規化仍可能影響內積；第 14 章會實際計算。

## Index 與 Embedding 不同

向量是表示，索引是用來快速搜尋表示的資料結構。你可以先線性比較所有向量，再建立 HNSW；建索引不會重新學到語言語意，也不會修復錯誤 pooling。

## 練習與參考答案

**題目：**一個模型輸出 `(2,128,768)`，可否說它給了兩個 128 維句向量？

**參考答案：**通常這代表兩個樣本、各 128 個位置、每位置 768 維。要先確認 API 定義，再按 recipe 得到整句表示。不能只根據維度數量猜軸的含義。
