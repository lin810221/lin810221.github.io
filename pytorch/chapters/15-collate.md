# Collate、Padding 與 mask：把變長資料變成 batch

定義 PAD、有效位置與平均分母，讓不同長度序列能正確一起運算。

## 為什麼預設堆疊會失敗

兩個 token list 長度分別 2 與 3，無法直接 stack 成一般矩形 Tensor。collate_fn 接收一批樣本 list，將內容整理成模型可接受的契約。本課使用 PAD=0，真實 token 從 1 開始，輸出 tokens[N,T]、mask[N,T] 與 labels[N]。

## 看懂補零後的意義

序列 `[1,2]` 與 `[3]` 變成 `[[1,2],[3,0]]`，mask 為 `[[True,True],[True,False]]`。PAD 的 embedding 可設 padding_idx=0 以免更新該列，但若最後對兩個位置直接 mean，第二句仍被多除了一次。因此需要 mask 與有效 token 計數，而不只是將 PAD 向量設零。

$$
h_i=\frac{\sum_t m_{i,t}e_{i,t}}{\sum_t m_{i,t}}
$$

分母為零時本課直接拒絕全空序列。正式系統可以設計 EMPTY token 或回傳明確狀態，但不能默默用無意義值冒充有效表示。

## 介面與模型要一起約定

mask 的 True 代表有效，是本課模型的契約。其他 Attention API 的 bool mask 可能有不同語意，不能看到 mask 就直接搬用。長度、截斷位置、PAD ID、詞表大小與 label mapping 都應寫進設定，推論時沿用。

## 批次效率與資料損失

長短差很多的序列補到同一最大長度，會浪費計算。可依長度分桶、限制 token budget 或動態 batch，但這會改變 sampler 與有效樣本數。截斷也可能丟掉關鍵訊息，必須評估，而非只追求不 OOM。

## 練習與解答

給定 embedding 第一個 token `[2,0]`、第二個 `[0,2]`，兩者 mean 為 `[1,1]`；加入兩個 PAD 後仍應 `[1,1]`。若變 `[.5,.5]`，你平均了 padded length。測試套件會檢查增加 PAD 不改預測，以及 padding embedding 的梯度為零；這是行為測試，比只檢查張量有三個維度更有意義。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/06_collate.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:06_collate.py -->

## 官方來源與延伸閱讀

- [DataLoader collate](https://docs.pytorch.org/docs/2.15/data.html)
- [Embedding 與 padding](https://docs.pytorch.org/docs/2.15/nn.html#sparse-layers)
