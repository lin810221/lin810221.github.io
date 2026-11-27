# 矩形因果遮罩與數值等價

<figure class="tf-figure"><a href="assets/figures/17-cache-offset-mask.svg" target="_blank" rel="noopener"><img src="assets/figures/17-cache-offset-mask.svg" alt="K與V各有舊位置0,1,2及新位置3,4，本次兩query的5欄允許遮罩分別11110與11111。" loading="lazy"></a><figcaption>KV cache與非正方形因果遮罩。快取不只省重算；正確性取決於key位置、query位置與遮罩的對齊。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>核對past、新query、key與位置的關係，先寫出shape和允許矩陣，再討論容量或效能。 本頁主題：矩形因果遮罩與數值等價。</p></div>

快取實作最重要的驗收，是同一模型在完整與分段計算時，對相同位置給出一致logits。

## 因果條件帶著偏移

past長P，新query長Q，key長 $K=P+Q$ 。新query的局部列i對應全域位置 $P+i$ ，允許的key條件為 $j\le P+i$ 。不是 $j\le i$ ；後者是左上對齊，會錯誤遮掉已存在的前綴。

$$
M_{ij}=\mathbf 1[j\le P+i],\quad i\in[0,Q),\ j\in[0,P+Q)
$$

$P=3$、$Q=2$時，第一列11110，第二列11111；$Q=1$時，唯一新query可以看所有past與自己。不要因為只有一列就以為應該只看第一個key。

## SDPA的明確做法

本課用bool allowed mask、 `is_causal=False` 、 `dropout_p=0` 做推論。PyTorch SDPA的非方形 `is_causal=True` 按左上對齊，和cached尾段需求不同。MultiheadAttention的bool True又代表阻擋，不能把同一矩陣不取反就跨API使用。

07_sdpa_masks.py把explicit mask結果和手寫softmax參考比較，再故意用錯的矩形is_causal，讓差異可觀察。手寫參考對完全沒有合法key的列報錯，而不是讓softmax(-inf,...)產生NaN。

## 比較完整與分段

17_cache_equivalence.py先算五個token的完整logits，再prefill前三個、追加後兩個。比較完整路徑[:,3:]和chunk logits；不只看最後argmax。先測chunk長2能揭露chunk內未來洩漏，再測逐token、不同batch及長度。

誤差需同時看absolute與relative tolerance。相同CPU float32可能只有極小差異，不代表所有GPU或低精度都逐位元一致。若差異大，先定位第一層不同的張量，再看位置、cache順序、dtype與mask。

## 練習與解析

past2、新3，允許列應為11100、11110、11111。若第一列11111，第一個新token看到了後兩個新token，破壞因果；若第一列10000，又把合法前綴遮太多。兩種錯誤都可能仍得到有限輸出。

相同生成文字但logits差很大，是否能驗收？不能。只是目前最高分未翻轉，換prompt、門檻或取樣就可能不同。數值等價是機制檢查，生成一致是額外觀察。

## 原始資料與查核

[SDPA矩形定義](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)；[lower-right bias](https://docs.pytorch.org/docs/2.15/generated/torch.nn.attention.bias.causal_lower_right.html)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 07_sdpa_masks.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:07_sdpa_masks.py -->

