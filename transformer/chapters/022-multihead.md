# 多頭Attention與形狀重排

<figure class="tf-figure"><a href="assets/figures/07-qkv-numerical.svg" target="_blank" rel="noopener"><img src="assets/figures/07-qkv-numerical.svg" alt="查詢1和兩個key1,0得到分數1,0，softmax為0.7311,0.2689，再用此顯示權重加權V兩列2,0與0,4得到1.4622,1.0756。" loading="lazy"></a><figcaption>Q、K、V：先找關聯，再聚合內容。自己改一個V值，確認權重不變而輸出改變；再改K值觀察權重。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>依Q、K、V與遮罩逐步計算；核對每列權重分母、head軸和可見位置。 本頁主題：多頭Attention與形狀重排。</p></div>

## 多個投影子空間共同看同一段輸入

多頭Attention讓同一批位置經不同可學投影產生多組Q/K/V，各自計算權重與混合，再將結果串接、經輸出投影整合。頭不是預先指定的文法角色，也不保證一頭永遠只看主詞、另一頭只看時間；這些若要宣稱，需要實驗證據，不能從名稱推導。

標準等寬設計中$D=H\times d_h$。固定D時增加H會減小每頭寬度，不是免費讓每頭都維持同樣寬度再無成本增加能力。不同架構可有不等寬、GQA等安排，本單元先學最基本Q/K/V頭數相同的MHA。

## 從[B,T,D]拆成[B,H,T,d_h]

 $B=2$ 、$T=3$、$D=8$、$H=2$，投影後Q是`[2,3,8]`。先reshape成`[2,3,2,4]`，再transpose時間與頭軸，得到`[2,2,3,4]`。這樣每個頭的三個Token仍對齊自己的通道；不是把六個Token分成兩段不同句子。

```python
import torch

q = torch.arange(2*3*8).reshape(2, 3, 8)
heads = q.reshape(2, 3, 2, 4).transpose(1, 2)
assert heads.shape == (2, 2, 3, 4)
restored = heads.transpose(1, 2).reshape(2, 3, 8)
assert torch.equal(restored, q)
```

如果直接把`[B,H,T,d_h]`reshape回`[B,T,D]`，不先把 $\frac{H}{T}$ 轉回，可能混合不同位置的通道，shape卻仍合法。這個往返測試能抓出重排錯誤，比只檢查最終shape更嚴格。

## 每頭權重與最後輸出

 $\frac{Q}{K}$ 分數shape是`[B,H,T_q,T_k]`，softmax沿最後key軸；Value混合得到`[B,H,T_q,d_h]`。合頭回`[B,T_q,D]`後，乘W_O=`[D,D]`，讓不同頭的通道共同影響輸出。W_O是矩陣，不只是給每個頭一個固定重要性分數。

同一份causal allowed`[T_q,T_k]`可按規則廣播到各batch與頭；若還有每段不同padding，需引入batch軸。測試要改動單一batch或單一頭的資料，確認不會意外污染其他不相關分組。

## 標準MHA參數量

若Q/K/V與輸出投影都是D到D、無bias，四個矩陣共 $4D^{2}$ 個參數；$D=8$時為256。改H但保持D與這四個投影尺寸，這個參數數不因頭數直接加倍。若有bias則另計4D；如果採不同 $\frac{K}{V}$ 寬度或共享設計，公式需相應更改。

在固定D的基本設計下，主要Attention乘法約隨 $T^{2}D$ 成長，概念權重矩陣元素數為 $BHT^{2}$ 。實際高效後端可能避免完整實體化權重；這不表示數學上不再比較位置，也不能用手寫權重矩陣記憶體直接預言所有後端實測。

## 多頭可解釋性與測試界線

觀察每頭熱圖可幫排錯，但平均頭權重可能掩蓋差異，且權重本身不是完整因果解釋。若API只回傳平均權重，需先查設定，不能把一張圖當成所有頭相同。輸出還經Value與W_O，熱圖高權重不必然代表對最終詞彙logit影響最大。

練習：$D=12$、$H=3$， $d_{h}=4$ ；若H改4，d_h變3，縮放改成 $\frac{1}{\sqrt{3}}$ 。不應保留原來 $\frac{1}{\sqrt{4}}$ 又宣稱只是換頭數而其他完全一樣。再問：$D=10$、$H=3$，能否整除後直接用3？不能，那會遺失一維，應拒絕或重新設計投影寬度。

## 原始介面與交付

保存每次reshape／transpose的軸名、投影矩陣shape與bias設定；用非巧合尺寸核對手寫逐頭版本和向量化版本。官方介面見[MultiheadAttention](https://docs.pytorch.org/docs/2.15/generated/torch.nn.MultiheadAttention.html)，排列操作見[transpose](https://docs.pytorch.org/docs/stable/generated/torch.transpose.html)。本單元只建立標準MHA，後續架構差異要按實際config判斷。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 08_multihead_shapes.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:08_multihead_shapes.py -->

