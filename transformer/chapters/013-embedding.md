# TokenEmbedding與查表

<figure class="tf-figure"><a href="assets/figures/05-embedding-tied-output.svg" target="_blank" rel="noopener"><img src="assets/figures/05-embedding-tied-output.svg" alt="六列三維Embedding表中ID1與ID4資料列被選出，右側隱狀態h乘同一E轉置得到V個logits。" loading="lazy"></a><figcaption>Embedding查表與輸出權重共享。追蹤ID、向量與logits的形狀；權重共享仍需保存詞表順序。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>找出查表、維度或位置的作用，說明它如何改變本頁的輸入表示與輸出分數。 本頁主題：TokenEmbedding與查表。</p></div>

## 整數ID本身沒有連續語意

Token ID100和101只是兩個詞彙項目的編號，不能因相差1就說意思較接近。Embedding建立`[V,D]`可學表，每個ID取出對應一列D維向量。輸入`[B,T]`整數IDs，輸出`[B,T,D]`浮點表示；查表不是把ID乘上一個連續比例，也不是把文字直接壓成神祕的單一數值。

本課固定byte主線V=259，包含三個控制ID與256個byte項目。若改用合併後BPE，V必須改成對應詞彙大小，並在模型建立前固定ID語意。兩份詞彙表即使大小相同，ID排列不同也不能直接共用原Embedding權重。

## 一張小表就能手動核對

假設V=4、$D=2$，表E為`[[0,0],[1,0],[0,1],[1,1]]`，輸入IDs`[1,3,1]`，輸出是`[[1,0],[1,1],[1,0]]`。相同ID在初始查表時拿到相同向量；但後面加位置與經Attention後，三個位置的上下文表示可以不同。

```python
import torch
from torch import nn

embedding = nn.Embedding(4, 2)
with torch.no_grad():
    embedding.weight.copy_(torch.tensor([[0.,0.],[1.,0.],[0.,1.],[1.,1.]]))
ids = torch.tensor([[1, 3, 1]], dtype=torch.long)
out = embedding(ids)
assert out.shape == (1, 3, 2)
assert torch.equal(out[0, 0], out[0, 2])
```

這是原創查表例，還未加入位置或上下文。把這種初始Token向量與句向量、整段文件Embedding混為同一東西，容易誤判模型能表示什麼。

## 重複索引的梯度會累加

若loss是上面所有輸出元素相加，ID1被查兩次，該列每一維的梯度為2；ID3查一次，梯度為1；未查列在這條查表路徑沒有貢獻。這說明參數共享：同一詞彙項目在不同位置的學習訊號一起更新同一列，而不是每個出現位置各有一套Embedding參數。

若Embedding同時綁到輸出頭，未出現在輸入的列仍可能因輸出分類路徑得到梯度。`padding_idx`只規範Embedding查表這一條路徑的梯度行為，不應概括成「該列無論如何都不會被任何其他共享用途更新」。共享參數的來源要沿計算圖追蹤。

## 向量維度不必有固定的人類標籤

訓練後某些向量在幾何上可能有規律，但第7維並不保證永遠代表情緒、第8維永遠代表顏色。表示可在多維中分散編碼，後續投影與非線性共同決定用途。相似度分析是觀察工具，不是給每一維硬貼語意名稱的證據。

同一個Token在不同句子可能有不同意思，初始查表不會自動為每種意思切換列；Transformer透過上下文運算形成位置特定表示。這也是為什麼只取原始Embedding列平均，和使用某個完整模型產生句向量，並不等價。

## 詞彙大小、模型寬度與成本

Embedding參數數為V×D。玩具V=259、$D=32$，共8288個元素；若每元素float32，原始權重約33152 bytes，不含梯度、最佳化器狀態與Tensor管理成本。D增加會影響後面各層，不只是這張表；V增加則影響輸出分類成本與詞彙語意。

練習：若輸入`[2,2,3]`，loss對每個查到向量取總和，沒有權重綁定也沒有padding特例，哪列梯度較大？ID2列為2、ID3列為1，其餘0。若實測不同，先查loss reduction、共享輸出頭與是否清零，再懷疑Autograd。

## 官方介面與跨課閱讀

參數、padding與索引行為見[PyTorch Embedding](https://docs.pytorch.org/docs/2.15/generated/torch.nn.Embedding.html)。更廣的向量學習、檢索與句表示可讀[Embedding課程](../embedding/index.html)；本課聚焦Token查表如何進入Transformer，不將查表本身描述成完整語言理解。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 04_embedding_head.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:04_embedding_head.py -->

