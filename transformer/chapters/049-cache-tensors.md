# KVCache實際保存哪些張量

<figure class="tf-figure"><a href="assets/figures/17-cache-offset-mask.svg" target="_blank" rel="noopener"><img src="assets/figures/17-cache-offset-mask.svg" alt="K與V各有舊位置0,1,2及新位置3,4，本次兩query的5欄允許遮罩分別11110與11111。" loading="lazy"></a><figcaption>KV cache與非正方形因果遮罩。快取不只省重算；正確性取決於key位置、query位置與遮罩的對齊。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>核對past、新query、key與位置的關係，先寫出shape和允許矩陣，再討論容量或效能。 本頁主題：KVCache實際保存哪些張量。</p></div>

KV cache保存每層已處理token的key與value，讓後續decode重用前綴計算；它不是檢索文件或整段答案的資料庫。

## 每層一份K與V

對MHA，每層cache常為K、V各[B,H,T,Dh]。Q只服務當前query，通常不為未來decode持續保存。下一個token在第l層的K/V必須由該層表示產生，不可把第一層K/V直接拿給所有層。

本課模型以list儲存每層tuple(K,V)。一個3-token prefix、2層、4heads、Dh8、batch1，會有兩組各[1,4,3,8]的K與V。新送2tokens後，沿序列軸串接成[1,4,5,8]，不是沿head或feature軸串接。

## 為何能重用

在固定權重、相同前綴、causal attention和相同位置下，過去token的表示不受未來影響，因此過去K/V可重用。若修改前綴、位置政策、模型權重或某層狀態，原cache不一定有效。這是需要明確驗證的等價條件。

cache仍可能占大量記憶體；越長prefix或更多同時請求，保存量越大。它減少前綴重算，不消除新token的投影、FFN、讀取K/V及attention運算。

## 只送尚未處理的部分

先prefill三個token取得cache，下次送第四個token。若把完整四個token再次送入同一cache，就把前綴重複追加，長度與位置都錯。框架cache也可能原地改動，同一物件不可在兩條測試路徑間共享後假裝未受污染。

以17_cache_equivalence.py看手寫模型，25_hf_cache.py看Transformers5.24的DynamicCache。兩者介面不必一樣：本課統一用cache概念，但正式API以實際版本核對，舊past_key_values名稱另有棄用狀態。

## 訓練與cache

一般teacher-forced全序列訓練可以平行計算causal目標，不必用推論cache逐token訓練。推論時用eval與inference_mode避免累積計算圖；若保留帶梯度cache跨很多步，會改變訓練圖與記憶體需求，不能視為免費優化。

## 練習與解析

把cache中的K和V互換，shape相同是否代表可用？不代表。K參與相似度分數，V參與加權聚合，兩者角色不同。測試要比實際logits，不只比shape。

若只比較cache長度為5，還不能證明內容與完整forward相同。下一單元將同時檢查矩形遮罩、位置與數值，讓快取從效能名詞變成可驗證的機制。

## 原始資料與查核

[KV cache解釋](https://huggingface.co/docs/transformers/en/cache_explanation)；[DynamicCache版本原始碼](https://github.com/huggingface/transformers/blob/v5.24.0/src/transformers/cache_utils.py)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 17_cache_equivalence.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:17_cache_equivalence.py -->

