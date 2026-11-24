# 逐Token生成與訓練平行化

<figure class="tf-figure"><a href="assets/figures/15-prefill-decode.svg" target="_blank" rel="noopener"><img src="assets/figures/15-prefill-decode.svg" alt="prefill我喜歡建立KV，decode第一步新產生貓，第二步把貓接回前綴再產生句點，舊前綴以淡色顯示。" loading="lazy"></a><figcaption>自回歸生成：先讀前綴，再逐字延伸。分開量測prefill與decode；不能把整段生成視為一次完全平行的前向。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>分開模型分布與解碼政策，指出本頁改變的是機率、候選集合、搜尋還是停止條件。 本頁主題：逐Token生成與訓練平行化。</p></div>

自迴歸模型把一段文字的機率拆成依序的條件機率；生成每一步依賴已經決定的前綴。

## 機率分解

$$
p(x_1,\ldots,x_T)=\prod_{t=1}^{T}p(x_t\mid x_{<t})
$$

這是鏈式法則，模型用神經網路近似各條件分布。訓練時正確前綴已知，可在一個causal forward同時計算許多位置的目標，常稱teacher forcing；不代表每個位置能看到未來target。

生成時先用prompt算最後位置的logits，選出新token，接回前綴，再預測下一個。第t+1個輸出還沒決定前，不能把它當正確輸入使用。因此單一序列的decode有順序依賴；多個序列或推測候選可平行，是另外的機制。

## 一個短例子

前綴[BOS,red, bird]的最後logits對詞表給出分數；選moves後，前綴多一個token，模型再預測句點。實際byte模型不會把red或bird當一個詞，這裡只是可讀的token符號算例，真實ID以tokenizer結果為準。

模型每次輸出的是整個詞表分布，不是預先存好下一句。greedy只取最高分，取樣則用分布與RNG做決策。同一權重在不同解碼設定下可產生不同文字，不能把它們都歸因於「模型變聰明」。

## 訓練與推論的落差

訓練多以真實前綴作條件，生成則會看到自己的錯誤輸出，錯誤可繼續影響後面。這與曝光偏差等問題有關，但不代表每個錯誤都能靠提高temperature解決。資料、目標、後訓練與解碼各有角色。

每個token的機率也不等同於整個答案為真的機率。常見字串容易被預測，不代表事實被查證。之後評估章會把語料似然與任務正確性分開。

## 執行與檢查

16_generation.py用未訓練模型檢查greedy的cached／uncached token序列是否相同，另展示固定seed的取樣IDs。未訓練模型可能偏向重複，這是機制展示，不是自然語言品質。真正看學習後生成，請先跑12_train_tiny_lm.py。

## 練習與解析

模型同時輸出[B,T,V]，為什麼生成只取最後位置？因為較早位置對應前綴內已知token的下一步目標；當前要延伸的是整個prompt的末端。如果batch有右padding，最後物理位置可能不是最後有效token，需依每筆長度選取，不能一律[-1]。

EOS、長度上限與外部停止條件都可能結束生成，原因應分開記錄。因長度截斷而停止，不表示模型完成了句子。

## 原始資料與查核

[GPT類語言模型目標](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)；[生成策略文件](https://huggingface.co/docs/transformers/en/generation_strategies)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 16_generation.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:16_generation.py -->

