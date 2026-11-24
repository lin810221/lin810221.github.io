# CrossAttention與SDPA介面

<figure class="tf-figure"><a href="assets/figures/10-attention-provenance.svg" target="_blank" rel="noopener"><img src="assets/figures/10-attention-provenance.svg" alt="三列分別把來源序列或目標前綴作為QKV，cross attention則用目標隱狀態作Q而encoder輸出作KV。" loading="lazy"></a><figcaption>Encoder、Decoder與Cross-Attention。cross-attention的矩陣形狀是目標長度×來源長度，別套用同長度self-attention直覺。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>依Q、K、V與遮罩逐步計算；核對每列權重分母、head軸和可見位置。 本頁主題：CrossAttention與SDPA介面。</p></div>

## Query與記憶來源可以不同

翻譯時，正在生成的目標序列可提供Q，完整來源句的encoder表示提供K/V，這就是常見CrossAttention。若目標有T_q=2個位置、來源有T_k=3個位置，分數是2×3；輸出長度跟query走，不是跟來源長度走。來源padding仍不可讀，但通常不需套目標與來源位置的普通下三角。

自回歸Decoder自己的SelfAttention仍要causal；CrossAttention能讀完整來源是因為來源在生成開始前已知。這兩個模組的可見性條件不同，不是Decoder所有Attention都一律封住右上角。若來源也是逐步串流，則需另一份明確可見性設計。

## 一組可核對的張量

令Q為`[B=1,H=1,T_q=2,d_h=2]`，K為`[1,1,3,2]`，V為`[1,1,3,1]`。以下示範不下載模型的基本介面，mask的True表示允許；正式範例另有測試與誤差容忍。

```python
import math
import torch
from torch.nn import functional as F

q = torch.tensor([[[[1., 0.], [0., 1.]]]])
k = torch.tensor([[[[1., 0.], [0., 1.], [1., 1.]]]])
v = torch.tensor([[[[2.], [4.], [8.]]]])
allowed = torch.tensor([[True, True, False], [True, True, False]])
scores = (q @ k.transpose(-2, -1)) / math.sqrt(2)
scores = scores.masked_fill(~allowed, float("-inf"))
reference = scores.softmax(dim=-1) @ v
actual = F.scaled_dot_product_attention(
    q, k, v, attn_mask=allowed, dropout_p=0.0, is_causal=False
)
assert actual.shape == (1, 1, 2, 1)
assert torch.allclose(actual, reference, atol=1e-6, rtol=1e-5)
```

第三個來源Value8雖很大，但被mask封鎖，不該影響輸出。改變它後結果應不變；這個不變性比只看輸出有限更能驗證mask。

## SDPA只負責Attention核心

`scaled_dot_product_attention`接收已形成的Q/K/V，不替你建立Token Embedding、投影矩陣、RoPE、合頭、W_O或殘差。它不是完整Transformer層，也不會自動理解文件邊界或聊天角色。你提供什麼shape、位置與mask，它就按該契約計算。

函式預設尺度依Q/K最後維度；布林mask True允許、float mask加入分數。與MHA的布林遮罩方向相反，移植時要明確轉換。對有cache的矩形causal情境，使用前一單元推導的絕對位置allowed，不把非方形is_causal直接當成後綴對齊。

## eval不會替函式改dropout_p

SDPA依你傳入的dropout_p執行，即使包住它的模組已eval，也要由forward把p設成0。常見寫法是`p if self.training else 0.0`。若測cached與完整前綴時忘記關閉dropout，隨機差異可能掩蓋真正的mask錯誤，或讓你誤判正確實作不一致。

相反地，訓練若永遠硬寫dropout_p=0，也不是有設定Dropout參數就自動生效。要以實際呼叫值與模式測試，不能只看config中有一個p欄位便宣稱正則化已使用。

## 後端相容與數值誤差

SDPA可能依裝置、dtype與shape選擇不同後端；數學上相同不保證浮點結果逐位一致。先在小尺寸CPU、dropout0與適當精度對照手寫參考，再用容忍誤差檢查目標環境。不要把可選融合kernel在特定GPU上的效能，直接當成本課CPU實測。

練習：改上例第三個Value為8000，結果應如何？仍不變，因它被封鎖。若先把mask當MHA語意反轉，則可能只讀第三個來源，輸出突然變8000，這是非常清楚的接口錯誤。再將Q長度改1、K保持3，確認輸出長度1，沒有暗中套錯方形假設。

## 原始來源

版本化介面見[PyTorch 2.15 SDPA](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)，CrossAttention的歷史脈絡可讀[對齊與翻譯原始論文](https://arxiv.org/abs/1409.0473)。本文小張量是原創算例，不涉及外部權重或API。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 07_sdpa_masks.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:07_sdpa_masks.py -->

