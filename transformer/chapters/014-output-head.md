# 語言模型輸出頭與權重綁定

<figure class="tf-figure"><a href="assets/figures/05-embedding-tied-output.svg" target="_blank" rel="noopener"><img src="assets/figures/05-embedding-tied-output.svg" alt="六列三維Embedding表中ID1與ID4資料列被選出，右側隱狀態h乘同一E轉置得到V個logits。" loading="lazy"></a><figcaption>Embedding查表與輸出權重共享。追蹤ID、向量與logits的形狀；權重共享仍需保存詞表順序。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>找出查表、維度或位置的作用，說明它如何改變本頁的輸入表示與輸出分數。 本頁主題：語言模型輸出頭與權重綁定。</p></div>

## 每個位置的向量如何變成候選分數

Transformer最後的隱藏狀態通常是`[B,T,D]`，語言模型頭把每個D維向量投影到V個詞彙分數，得到`[B,T,V]`。若採數學列向量記法，可寫$Z=HW_{out}+b$，其中$W_{out}$為`[D,V]`，b可有可無。PyTorch Linear權重儲存為`[V,D]`，所以常以隱藏向量乘該權重轉置計算。

這一步輸出的是logits，不一定已softmax。訓練交叉熵可直接接收logits；生成才依解碼政策轉分布或排序。若只保留argmax ID，會丟失候選分布，不利於計算NLL、溫度抽樣與校準分析。

## 一個完全可手算的詞彙頭

令隱藏向量h=`[1,2]`，輸出權重三列為`[[1,0],[0,1],[1,1]]`，無bias。三個logits是`[1,2,3]`；softmax約`[.0900,.2447,.6652]`。第三個Token最可能，但它不是唯一可選結果。若所有logits同加100，softmax仍相同，顯示絕對位準不等於機率。

詞彙順序要與Tokenizer完全一致。若把第三列錯配成另一個ID，模型數值計算仍可能正常，文字語意卻整體錯位。保存模型時，權重、config、Tokenizer與特殊ID是一套工件，不能只備份某個Tensor檔就宣稱能重現完整生成。

## 權重綁定共享同一張表

當輸入Embedding為E=`[V,D]`，可令輸出Linear的weight直接共用E，logits為$HE^\top$。這叫weight tying；不是所有模型都必須採用，是否綁定要看具體架構與config。[Press與Wolf的原始研究](https://arxiv.org/abs/1608.05859)是這項語言模型設計的歷史來源。

如果V=100、$D=8$，不綁定時輸入表與無bias輸出頭共1600個元素，綁定後獨立元素只有800。若另有輸出bias，仍要加100。這裡只計這兩個模組，不是整個Transformer參數量；後面Attention、FFN與Norm仍需另外計算。

## copy與share不是同一件事

把輸出頭數值複製成Embedding的初始值，只保證那一刻相同；之後兩者若是獨立Parameter，會沿不同梯度更新。真正綁定要共享同一Parameter，而不只是`copy_`。驗收時可檢查物件關係與一次更新後是否仍共享，計參數時也要避免同一物件算兩次。

```python
from torch import nn

embedding = nn.Embedding(10, 4)
head = nn.Linear(4, 10, bias=False)
head.weight = embedding.weight
assert head.weight is embedding.weight
```

這個示例只建立共享關係，不代表任意模型都允許這樣替換。若hidden寬度與Embedding寬度不同，需要額外投影或不同設計；若輸出詞彙不是同一表，也不能強行綁定。

## 共享讓梯度來源相加

同一張表一方面用於輸入查表，另一方面參與所有候選logits，因此其梯度包含兩條用途的貢獻。沒有出現在輸入的Token仍可能由輸出softmax得到梯度。PAD的查表特例也不等於該列在共享輸出頭完全不參與計算，若要禁止生成PAD，還有解碼或訓練政策要明定。

綁定後節省參數，但不代表所有中間logits或輸出計算都消失；仍需要對V個候選評分。語言模型的計算與記憶體成本，不能只以儲存權重節省比例推論。

## 練習與解析

V=259、$D=32$，無bias且共享輸入輸出，這兩處共多少獨立參數？答案8288，不是16576。若state_dict有兩個名稱指向相同權重，也不代表真的有兩套獨立參數；序列化工具對共享的保存規則需另外查核。

再問：輸出logits=`[1,2,3]`，正確類是第二類，loss是否因最高類錯誤就固定為1？不是。交叉熵為`−ln(.2447)≈1.4076`，反映正確類分配到的機率。介面見[Linear](https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html)與[CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 04_embedding_head.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:04_embedding_head.py -->

