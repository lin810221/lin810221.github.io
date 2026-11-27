# Cache與容量練習解析

<figure class="tf-figure"><a href="assets/figures/18-mha-gqa-mqa.svg" target="_blank" rel="noopener"><img src="assets/figures/18-mha-gqa-mqa.svg" alt="MHA八個query分別對八KV組，GQA每兩query共用一組共四組，MQA八query共一組；快取4,2,0.5MiB。" loading="lazy"></a><figcaption>共享 $\frac{K}{V}$  heads，改變cache容量。記憶體公式使用Hkv而不是Hq；GQA還需核對整除關係與實際kernel支援。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>核對past、新query、key與位置的關係，先寫出shape和允許矩陣，再討論容量或效能。 本頁主題：Cache與容量練習解析。</p></div>

這組練習同時檢查shape、遮罩、位置與資源分母，避免只驗證cache物件存在。

## 題目：追加軸

 $\frac{K}{V}$ 原為[2,4,3,8]，新token的 $\frac{K}{V}$ 為[2,4,2,8]，應沿哪一軸串接？解析：沿序列軸-2，結果[2,4,5,8]。沿最後一軸會變head_dim並破壞點積；沿head軸則改模型結構。

## 題目：遮罩逐列

past1、新3時，key長4，允許列為1100、1110、1111。SDPA True表示可參與，MHA bool遮罩則要相反。分數乘0並非遮蔽，因為exp0仍有正值；需要API定義的mask或加負無窮。

## 題目：兩種長度

右padding後物理cache長5，某句只有3個有效token；追加一個新token時，本課位置表用3，但cache物理新增欄位在5。完整key mask需長6，保留原兩格padding False。這與只送一個新mask True不同。

## 題目：計算容量

B1、L2、S1024、Hkv8、Dh64、b2，純 $\mathrm{KV}=2,097,152\mathrm{bytes}=2MiB$ 。若改float32為4MiB；若只是把query heads增加，Hkv與Dh不變，純KV公式不因此改變，但query相關計算可能增加。

## 實作任務

依序跑07_sdpa_masks、17_cache_equivalence、18_padding_positions、19_gqa與20_kv_capacity。記錄explicit mask與參考的誤差、cached與full logits差、最後有效位置、GQA對照和容量。完整檔名見範例包。

故意把past偏移設0，再觀察哪個測試先失敗；恢復後改變prefix，確認舊cache不應重用。錯誤實驗只在自己的本機副本進行，保留正確版本與測試結果供比較。

## 驗收條件

正確的cache不只是更快，還要在聲明條件下保持相同模型函數。若只在一個token上argmax相同，證據太少；應包含多token chunk、不同長度、padding、重複使用與context耗盡的情況。

本課未把CPU小範例的速度當生產服務承諾。下一章會介紹FlashAttention、分頁、量化與推測解碼，並分清楚哪些省計算、哪些省記憶體流量、哪些改排程。

## 原始資料與查核

[SDPA](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)；[Cache說明](https://huggingface.co/docs/transformers/en/cache_explanation)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。
