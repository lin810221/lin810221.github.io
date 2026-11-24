# causal與padding遮罩

<figure class="tf-figure"><a href="assets/figures/08-causal-padding-masks.svg" target="_blank" rel="noopener"><img src="assets/figures/08-causal-padding-masks.svg" alt="左矩陣是四乘四下三角True因果遮罩，右矩陣最後key為PAD全False，PAD query輸出另外忽略。" loading="lazy"></a><figcaption>因果遮罩與padding遮罩。檢查列欄方向和True的定義；padding key遮罩與loss忽略不是相同動作。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>依Q、K、V與遮罩逐步計算；核對每列權重分母、head軸和可見位置。 本頁主題：causal與padding遮罩。</p></div>

## 模型在預測時不能讀到答案

next-token訓練把整段已知文字放進Tensor，並不代表每個位置都能讀整段。位置i若要預測下一個Token，通常只能讀到自己與更早的有效內容；causal mask阻止它直接讀未來。若遮罩漏掉，訓練loss可能漂亮得不合理，但生成時沒有未來真值可偷看，表現就會崩潰。

Padding mask則排除人為補齊的key；文件mask限制讀取同一文件或同一對話片段。完整allowed規則可寫成「key有效、在允許文件、key邏輯位置不晚於query」。三個條件彼此獨立，不能只加一個下三角就假定padding與文件邊界都正確。

## 方形下三角的最小例子

$T=3$、位置0到2，允許矩陣是`[[1,0,0],[1,1,0],[1,1,1]]`。列是query、欄是key，對角線可見，因為位置i的輸入Token本來就是已知前綴的一部分；它預測的是下一Token，不是同位置已知ID。

若改成嚴格下三角、對角線也封鎖，第一列可能沒有任何key，且改變訓練條件。這不一定永遠是某種任務不能用的設計，但不是本課next-token主線的遮罩；你必須重新定義位置與監督，不能只因三角方向看起來差不多就替換。

## cache時是矩形，不是直接套左上三角

已有3個cache Token，本次加入2個新Token，K總長5、Q長2。query邏輯位置是3與4，key位置0到4，allowed應為`[[1,1,1,1,0],[1,1,1,1,1]]`。直接對2×5做普通tril會得到`[[1,0,0,0,0],[1,1,0,0,0]]`，把大部分合法前綴誤封鎖。

```python
import torch

past = 3
q_positions = past + torch.arange(2)
k_positions = torch.arange(5)
allowed = k_positions[None, :] <= q_positions[:, None]
assert allowed.tolist() == [[True, True, True, True, False],
                            [True, True, True, True, True]]
```

這裡以連續且等長cache的簡化位置表示；變長batch、左padding、滑動視窗與文件重設需要各自position_ids／有效性資訊。概念核心是比較邏輯位置，而非只看本次Q的局部索引。

## 不同API的True意思相反

PyTorch SDPA的布林`attn_mask=True`表示允許參與；`nn.MultiheadAttention`的布林attn_mask與key_padding_mask中，True則表示封鎖。遷移時要依API轉換，不把同一個bool Tensor直接拿去共用。加性float mask通常是加入分數的bias，0與−∞的語意又是另一種表示方式。

PyTorch 2.15的SDPA對非方形`is_causal=True`採左上對齊語意，因此不能把它直接當上例的cache offset遮罩；本課主線使用明確allowed mask，並在該呼叫讓is_causal=False。文件要求attn_mask與is_causal的相容條件也要遵守，不依未記錄的後端偶然行為。

## 無效query與NaN要有政策

若padding query列沒有合法key，不應在普通全−∞softmax後才到處補NaN。可只計有效query，或設計明確的安全佔位規則並將其輸出與loss排除；有效query沒有來源時則應拒絕設定。排除target的−100不會自動修復前面Attention已產生的NaN。

練習：將位置2以後的輸入Token任意改動，位置0與1的輸出是否應變？在eval、相同位置與純causal流程下不應。這個未來擾動測試比「mask長得像三角」更有說服力。再比較完整前綴與逐步cache，檢查矩形對齊；以兩種不同長度batch檢查padding隔離。

## 正式介面

請對照[SDPA 2.15](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)與[MultiheadAttention 2.15](https://docs.pytorch.org/docs/2.15/generated/torch.nn.MultiheadAttention.html)。此處明確限定版本與mask表示，不把一個框架的布林慣例寫成Attention數學的通用定義。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 07_sdpa_masks.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:07_sdpa_masks.py -->

