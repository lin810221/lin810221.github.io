# nextToken目標與標籤位移

<figure class="tf-figure"><a href="assets/figures/11-next-token-shift.svg" target="_blank" rel="noopener"><img src="assets/figures/11-next-token-shift.svg" alt="輸入BOS我愛貓PAD與目標我愛貓EOS忽略上下對齊，前四格箭頭相連，PAD loss不納入分母。" loading="lazy"></a><figcaption>Next-token訓練：輸入、目標與忽略位置。手寫一個樣本的X與Y；若目標和輸入同格未右移，任務就被改變了。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>指出每個target的來源、哪些項目計入loss，以及哪些資料不可跨越切分界線。 本頁主題：nextToken目標與標籤位移。</p></div>

## 每個位置的答案是下一個Token

給定序列S=`[BOS,A,B,EOS]`，手寫next-token主線取input=`[BOS,A,B]`、target=`[A,B,EOS]`。位置0讀BOS後預測A，位置1讀到A後預測B，位置2讀到B後預測EOS。causal mask允許位置讀自己的輸入，因為自己的輸入並不是該欄target，而是前一個已知Token。

如果input與target完全相同，又允許對角線，模型可能學成抄寫當前ID，loss下降卻沒有學會下一Token。若多位移一次，則變成隔一格預測，改了任務。最可靠的做法是印出小序列每個`input_prefix → target`配對，不只檢查shape。

## 本課byte算例

A的ASCII值65、B為66，byte IDs分別68與69；序列S是`[1,68,69,2]`。模型輸入`[1,68,69]`，輸出`[B=1,T=3,V=259]`logits，target是`[68,69,2]`。它不預測BOS之前不存在的字，也不把EOS後人為補的PAD當成一般原文監督。

Teacher forcing表示訓練時使用真實前綴輸入，而非每一步都先抽樣自己的Token再接回去。這使各位置可在一次causal forward中平行計算；生成時仍需逐步依已選Token延伸，兩種資料條件不完全相同。

## 交叉熵的類別軸

PyTorch交叉熵常接收`[N,C,...]`logits；本模型輸出`[B,T,V]`，可攤成`[B*T,V]`對`[B*T]`，或轉成`[B,V,T]`對`[B,T]`。不能把未轉置的`[B,T,V]`直接當`[B,C,T]`，否則可能沿錯軸，或在巧合尺寸下默默算另一個問題。

```python
import torch
from torch.nn import functional as F

logits = torch.zeros(1, 3, 259)
targets = torch.tensor([[68, 69, 2]], dtype=torch.long)
flat = F.cross_entropy(logits.reshape(-1, 259), targets.reshape(-1))
transposed = F.cross_entropy(logits.transpose(1, 2), targets)
assert torch.allclose(flat, transposed)
assert abs(flat.item() - torch.log(torch.tensor(259.)).item()) < 1e-5
```

均勻logits的每步正確機率1/259，所以loss約ln(259)；這是驗證損失軸與分母的原創控制例，不是已訓練模型的成績。

## PAD ID與−100的用途

input中的PAD是詞彙ID0；target不應監督的位置設−100，配合ignore_index。−100不是一個可生成的Token，也不能拿去查Embedding。若把−100先clamp成0，會把原本應忽略的目標變成PAD監督，改變loss與分母。

對話中只訓練assistant內容時，target mask也要跟位移後位置對齊。某個答案Token出現在原始序列第j格，它由前一位置j−1的logit預測；若直接把原始答案位置mask套到同欄logit，可能漏掉第一個答案、多算最後邊界。

## 手寫模型與高階模型只選一處位移

本課手寫模型由資料／loss程式明確建立X與Y，模型forward不再暗中shift。某些Hugging Face causal LM在傳labels時內部做shift，通常要求與input_ids對齊的未位移labels，再依其正式介面處理。不能把本課已位移target直接套進所有高階模型，造成shift兩次。

對照外部模型時，先查該版本的loss實作，使用三到四個Token的小例子核對每個logit對應目標。不同head或任務類別也可能有不同契約，不以「都是Transformers」推論。

## 練習與解析

S=`[1,10,20,2]`，某程式input=`[1,10,20]`，target=`[20,2,0]`，它是本課next-token嗎？不是，前兩欄已隔兩個位置，最後還把PAD當一般目標。正確target為`[10,20,2]`；若某位置無有效後繼，就以明確ignore政策處理，而不是隨意補0。

原始API見[PyTorch CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)，外部模型需查[Transformers 5.24.0 causal LM原始碼](https://github.com/huggingface/transformers/tree/v5.24.0/src/transformers/models)。位移是資料與模型之間的契約，請在README寫清楚只做一次。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 10_shifted_loss.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:10_shifted_loss.py -->

