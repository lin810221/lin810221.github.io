# 張量參數與容量速查

<figure class="tf-figure"><a href="assets/figures/31-tensor-complexity-map.svg" target="_blank" rel="noopener"><img src="assets/figures/31-tensor-complexity-map.svg" alt="五列表格將token hidden QKV dense scores cache對應形狀，dense scores平方長度，cache線性長度再乘dtypebytes。" loading="lazy"></a><figcaption>張量形狀、密集注意力與cache對照。估算時先確認物件：注意力工作矩陣、歷史KV與模型權重不是同一筆記憶體。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>選本頁一個概念對照圖中shape、公式或除錯分支，說出下一個需要核對的條件。 本頁主題：張量參數與容量速查。</p></div>

## 本頁符號

$B$是batch，$T_q$與$T_k$是query和key長度，$D$是模型隱藏維度，$H_q$是query heads，$H_{kv}$是KV heads，$d_h$是每head維度，$L$是層數，$V$是詞表大小，$F$是MLP中間維度，$C$是learned position表的context容量。先註明符號，再談平方或線性，才能避免把總長度和本次新增長度混在一起。

| 物件 | 常見形狀 | 先檢查什麼 |
|---|---|---|
| token IDs | B × T | int64，ID在詞表範圍內 |
| hidden states | $B\times T\times D$ | sequence與feature軸 |
| Q | B × Hq × Tq × dh | $D=Hq\times dh$ |
| K、V | B × Hkv × Tk × dh | GQA時head數不同 |
| attention scores | B × Hq × Tq × Tk | 列query、欄key |
| logits | B × T × V | 最後一維是詞表 |
| labels | B × T | 外部shift一次，忽略位置-100 |

GQA一般要求$H_q$可被$H_{kv}$整除，K與V的head數相同。MHA為$H_q=H_{kv}$，MQA為$H_{kv}=1$；不能把三種名稱當成相同的cache形狀。

## 預設TinyGPT參數量手算

本課預設$V=259,D=32,C=64,L=2,F=96$。Embedding有$VD=8288$個參數，learned position有$CD=2048$個。每個block的attention採無bias QKV與輸出投影，共$4D^2=4096$；兩個有bias的MLP線性層共$2DF+F+D=6272$；兩個LayerNorm各有gamma與beta，合計$4D=128$。每層總數10,496。

最後一個LayerNorm再加$2D=64$。因lm_head與embedding共用權重，不重複加一份$VD$，所以總數：

$$
VD+CD+L(4D^2+2DF+F+5D)+2D=31{,}392.
$$

這個值由當前架構定義推導，不是所有GPT的通則。若改成untied且無bias的輸出head，另加8288，總數39,680；若改SwiGLU、RMSNorm、bias或GQA，必須重新數。框架統計時也要避免把共享張量重複計數。

## KV cache純張量容量

假設每層K/V同shape與dtype、full attention且沒有量化，容量為：

$$
M_{KV}=2\times B\times L\times T_k\times H_{kv}\times d_h\times b.
$$

$b$是每元素bytes，前面的2代表K與V。以預設TinyGPT、batch1、長度64、4個KV heads、head_dim8、float32每元素4 bytes計算，純KV為32,768 bytes，也就是32 KiB。這不含權重、Q、attention工作空間、allocator或Python物件。

另一個獨立容量算例取$B=2,L=32,T_k=4096,H_{kv}=8,d_h=128,b=2$，結果1 GiB；若改成32個KV heads，便為4 GiB。這是公式估算，不是本課CPU小模型的記憶體實測。分頁metadata、batch padding、滑動視窗與量化都有自己的修正條件。

## 時間與工作記憶體要分開

完整dense self-attention的主要QK與AV算術約為$O(BT^2D)$；投影和MLP還有$O(BTD^2)$、$O(BTDF)$等成本。cache decode單次只有少量queries，但要讀歷史K/V；不能因query長度1就說每步完全不受context影響。

若把完整scores實體化，元素數為$B H_q T_q T_k$。FlashAttention類方法可以避免保存完整矩陣，減少資料搬運與中間記憶體，不代表所有dense attention算術都變成線性。判斷瓶頸需要裝置與kernel的實際量測，而不是只比較Big-O符號。

## 訓練狀態的簡化估算

float32權重、float32梯度與Adam兩份float32動量，核心張量約需每參數16 bytes。用31,392參數算得502,272 bytes，約490.5 KiB。這忽略step計數、暫存張量、activation、框架與allocator；optimizer狀態也可能在第一次更新時才建立。因此它是下層分項估算，不是整個Python行程的RAM需求。

若採混合精度，master weights、gradient dtype、optimizer實作可能不同，不能把所有欄位一律乘半。量化也可能需要scale、zero point與分組metadata；4 bit權重不表示整個模型服務只占原容量八分之一。

## 練習與解析

**題目：** 模型有8個query heads、2個KV heads，其他維度不變。學生用8代入KV公式，並把scores容量也稱為cache。如何修正？

**解析：** KV用2，所以學生在這一分項高估4倍；scores是當前query與key的配對工作矩陣，cache是跨步保存的K/V。兩者的長度、heads及生命週期不同。先分開列shape、dtype與是否保存，再討論峰值和持續占用。

## 參考與日期

查核日期：2026-11-24；參數與容量數字皆為明示架構的原創推算。

- [GQA原始研究](https://arxiv.org/abs/2305.13245)
- [FlashAttention原始研究](https://arxiv.org/abs/2205.14135)
- [PyTorch Linear參數定義](https://docs.pytorch.org/docs/2.15/generated/torch.nn.Linear.html)
