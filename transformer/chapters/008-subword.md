# BPEWordPiece與Unigram

<figure class="tf-figure"><a href="assets/figures/04-bpe-merges.svg" target="_blank" rel="noopener"><img src="assets/figures/04-bpe-merges.svg" alt="lower先分l o w e r，按順位合併l加o成lo，再lo加w成low，最後low e r。" loading="lazy"></a><figcaption>BPE：從較小片段到子詞。相同文字在不同詞表和規則下會有不同token數；版本需與模型一起保存。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>沿文字、byte與ID的轉換追蹤，說明哪些邊界、特殊符號或padding會影響本頁方法。 本頁主題：BPEWordPiece與Unigram。</p></div>

## 為何不直接一個詞一個ID

整詞詞彙表容易遇到新名字、拼字變化與多語言組合，詞彙數又可能很大；字元或byte詞彙表較小，序列卻會變長。子詞方法在中間取得取捨：常見片段用較少Token，罕見內容由較小單位組合。這不保證每個片段都有完整語意，也不表示切分邊界等於自然語言的詞界。

對Transformer而言，詞彙大小影響Embedding與輸出頭，序列長度影響Attention及訓練Token數。Tokenizer因此是模型設計的一部分，不能訓練完後任意換一份相同大小詞彙表，期待原權重仍知道每個ID代表什麼。

## BPE：依合併規則形成較大片段

BPE常從小單位開始，反覆選擇相鄰符號對合併；訓練得到有順序的merge規則，編碼再依這些規則處理新文字。文字子詞BPE與byte-level BPE的初始單位、前切分與解碼安排可能不同。[Sennrich等人的原始研究](https://arxiv.org/abs/1508.07909)是神經翻譯子詞BPE的歷史閱讀。

玩具訓練序列`a b a b`與`a b`中，pair(a,b)出現三次，pair(b,a)一次，先合併ab後，兩段變`ab ab`與`ab`。這只說明一輪相鄰合併；是否跨空白、如何同分破局、是否保留詞界，仍是具體Tokenizer政策。

## WordPiece：詞彙與最長可用片段

WordPiece常見推論是依既定詞彙表進行最長匹配，再對剩餘片段繼續切分；某些詞彙以`##`等慣例標記非詞首片段。這些可見字串是工具表示方法，不能把`##`想成所有Tokenizer都需要的自然語言符號。訓練目標與詞彙建立細節也有實作差異，不應用一個網路上的簡化分數公式概括所有版本。

假設詞彙有`play`與`##ing`，某套規則可把playing切成兩個片段；若缺少可覆蓋剩餘字串的詞彙，則依實作可能出現UNK。byte fallback與未知詞政策要另外確認，不能因它叫子詞方法就假定所有Unicode文字都能原樣往返。官方實作可查[Tokenizers WordPiece原始碼](https://github.com/huggingface/tokenizers/tree/v0.23.3/tokenizers/src/models/wordpiece)。

## Unigram：在多個可能切分間評分

Unigram子詞模型為片段賦予機率，字串可能有多種切分，再依分數選擇或抽樣。原創例子：四個片段a、bc、ab、c的機率分別.1、.3、.4、.2。字串abc可切成`a|bc`，乘積.1×.3=.03；也可切成`ab|c`，乘積.4×.2=.08。在這個簡化分數下後者較高。實際訓練包含候選詞彙、剪枝與機率估計，不能只用兩筆乘法當完整演算法。

[Kudo的原始論文](https://arxiv.org/abs/1804.10959)討論子詞切分的不確定性與取樣。訓練時可利用多種切分作正則化，但驗證與推論要明確指定是否採確定切分或抽樣，否則同一字串的Token數與loss可能無意變動。

## 工具與演算法分開命名

SentencePiece是工具系統，可支援不同子詞模型；「用了SentencePiece」並未完整交代使用BPE還是Unigram、正規化、空白政策與byte fallback。[SentencePiece原始論文](https://arxiv.org/abs/1808.06226)可作工具背景。Hugging Face Tokenizers也組合normalizer、pre-tokenizer、model、post-processor與decoder，多個元件共同決定結果。

請保存整份Tokenizer工件與版本，不只保存一個vocab文字檔。特殊ID、合併順序、正規化、截斷與聊天模板任一改變，都可能改變模型實際看到的序列。詞彙表同樣有5000列，也不代表兩份Token ID可以互換。

## 練習與解析

若把Tokenizer在train、validation與test合併語料上重新訓練，模型雖沒讀到test標籤，是否完全沒有洩漏？不能這樣說。Tokenizer已利用test文字分布選片段，改變了表示與壓縮；應按研究目標明定政策，課程自訓主線只用train學合併，之後凍結。

再問：子詞片段`ing`有時像後綴，是否每個Token都有可解釋語意？不一定。片段也可能是標點、bytes或統計常見組合，語意仍需上下文與模型表示共同形成。
