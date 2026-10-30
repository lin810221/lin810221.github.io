# 序列實作：Embedding、mask pooling 與文字分類

用小詞表練習token ID、PAD梯度與序列到類別的轉換。

## 從 token 到句子表示

輸入tokens[N,T]為long索引，Embedding把它轉成[N,T,D]，mask去除PAD後對有效位置平均，再由Linear(D,C)分類。這條路徑可完整訓練，與呼叫外部Embedding API不同。模型從這份極小合成資料開始學參數，不包含預訓練語言理解。

## 最小架構的能力限制

mean pooling忽略順序，[1,2]與[2,1]得到相同句向量。若任務需要語序，需加入RNN、位置資訊或Attention等架構。本課先把資料與梯度工程講清楚，更完整的Transformer理論由獨立課程承接。不要把詞袋式示範說成已具備大語言模型能力。

## Padding 的兩個測試

增加尾部PAD不應改變句子表示；padding_idx=0那一列的梯度應為零。本課測試對兩項都驗證。label float或token ID超出vocabulary時，應先修資料契約，不用clamp把所有未知詞默默改成最後一個token。正式tokenizer應定義UNK與PAD規則。

## 訓練與推論的相同契約

保存詞表／tokenizer版本、截斷長度、大小寫與正規化方式。推論沿用同一套ID，即使兩份詞表大小相同，只要ID對應不同，Embedding列的意義就全錯。這與向量模型的「同維度不代表同空間」有相似的工程風險。

## 練習與解答

讓`[1,2,0,0]`和`[1,2]`分別推論，比較logits，應在容許誤差內相同。把mean改成普通`.mean(dim=1)`後，結果開始依PAD長度改變，證明錯誤來自分母。再比較[1,2]與[2,1]，mean模型完全相同是架構限制，不是訓練不夠久。

最後嘗試用三類而非兩類標籤，修改head與資料，核對target範圍。不必為了擴類改Embedding的vocabulary，因為詞表大小與輸出類別數是兩個不同概念。執行本章範例，觀察loss與PAD梯度，而非只看模型印出幾個數。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/14_sequences.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:14_sequences.py -->

## 官方來源與延伸閱讀

- [Embedding 層](https://docs.pytorch.org/docs/2.15/nn.html#sparse-layers)
- [Pooling 與張量操作](https://docs.pytorch.org/docs/2.15/tensors.html)
- [表示學習課程](https://docs.pytorch.org/tutorials/beginner/nlp/word_embeddings_tutorial.html)
