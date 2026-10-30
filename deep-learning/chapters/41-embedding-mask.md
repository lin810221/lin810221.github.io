# Embedding、Padding與Mask：索引如何成為表示

把詞表、特殊ID與有效長度寫成可測契約。

## 查表而不是連續數值

token ID是離散索引，Embedding(V,D)回傳對應列，輸入long[N,T]→[N,T,D]。ID3不表示比ID2語意多一單位，不能直接當普通float特徵。詞表版本、PAD／UNK與清理規則是模型的一部分。

## PAD列與平均分母

padding_idx=0讓對應列在一般訓練不更新；若做mean pooling，仍需只除有效token數。補零後對所有T平均會讓短句表示依PAD量改變。全空序列要明確拒絕或設計EMPTY規則，不默默除0。

$$
u_i=\frac{\sum_t m_{i,t}e_{i,t}}{\sum_t m_{i,t}}
$$

## 本章兩項不變性檢查

第28例用[1,2,0,0]與[3,4,5,0]，masked pooling；第一句與只取[1,2]平均相同，PAD列grad為0。這比單看shape更能捕捉常見錯誤。若有weight decay或另行手工更新特殊列，也需按實際optimizer規則檢查。

## 長度與mask不能互相猜測

core raw序列只允許1..8，collate才加入0 PAD，所以長度明確。若合法token本身也可0，就不能再用tokens!=0推mask。Attention、loss與pooling對bool True的語意各有契約，不看名稱直接共用很危險。

## 表示的能力

mean pooling忽略順序，[1,2]與[2,1]相同；RNN／位置化Attention可引入順序。Embedding只是可學向量，不含自動預訓練語意；本課小詞表從隨機初值開始，沒有下載語言模型或聲稱理解自然語言。

## 練習與解答

給定兩個向量[2,0]、[0,2]，有效mean為[1,1]，加兩個PAD仍應相同。若變[.5,.5]，分母用了4。解答：檢查mask、有效長度及全空政策；換詞表時同維度不代表同ID意義，需一起版本化。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/28_embedding_mask.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:28_embedding_mask.py -->

## 原始論文與官方來源

- [Embedding與sparse layers](https://docs.pytorch.org/docs/2.15/nn.html#sparse-layers)
- [表示學習背景](https://www.deeplearningbook.org/contents/representation.html)
