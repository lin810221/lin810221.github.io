# 專題用現行框架核對模型介面

<figure class="tf-figure"><a href="assets/figures/30-cache-logits-parity.svg" target="_blank" rel="noopener"><img src="assets/figures/30-cache-logits-parity.svg" alt="完整前綴0,1,2,3前向與快取0,1,2加新位置3前向，底部以最大logit絕對差和容差比較。" loading="lazy"></a><figcaption>Cache正確性：對齊logits，不只看文字。先關閉dropout並控制位置與mask，再排查cache；相同文字也可能隱藏logit錯誤。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>依本頁專題追蹤資料、模型、固定輸入、數值比較與交付檔，寫出可重現的命令與限制。 本頁主題：專題用現行框架核對模型介面。</p></div>

## 為什麼手寫模型之後還要做這個專題

手寫TinyGPT讓你看見每個矩陣與mask；框架專題則檢查相同概念如何映射到現行公開實作。目標是能讀懂config、forward輸入、回傳物件、cache與序列化，而不是依賴一行自動下載來略過這些契約。本課以2026-11-24查核的Transformers 5.24.0為基準，將舊教學常見的參數名稱和目前原始碼分開處理。

執行入口：

```text
python transformer/examples/24_hf_offline_model.py
python transformer/examples/25_hf_cache.py
```

兩個程式明確使用本機小config和隨機初始化，不需要Hub模型權重；環境套件仍需先安裝。本段不把隨機模型稱為預訓練Llama，也不從它的輸出推論聊天或推理能力。

## 一定要覆寫預設大尺寸

`LlamaForCausalLM(LlamaConfig(...))`根據config建模。若直接採預設大規格，可能在還沒學會forward前就耗盡記憶體。本例明確設定vocab_size=300、hidden_size=32、intermediate_size=64、2層、4個query heads、2個KV heads、max_position_embeddings=64，並指定PAD/BOS/EOS為0/1/2。

它與本課TinyGPT不同：這裡用框架的Llama架構及GQA設定，不能把TinyGPT的learned position、LayerNorm或tied head假設直接套過去。需要哪些機制，應從該版本config與modeling原始碼確認。程式選eager attention以便在小CPU例中觀察數值；這不宣稱eager是所有裝置最快的實作。

## Forward輸出先看形狀

輸入`ids=[[1,30,31,2]]`有batch 1、長度4。輸出logits形狀應是$1\times4\times300$，每個位置有300個詞表分數。這個shape能由config與程式推導，數值是否正常仍需實際執行。採`use_cache=False`取得完整前向作為後續重讀與cache對照的參考。

最小紀錄包含輸入IDs、attention mask、position IDs、dtype、attention implementation和模型是否eval。只印模型類別名稱無法定位錯誤；取錯回傳欄位或把最後有效token與PAD混淆，也不是重裝套件能解決的問題。

## 5.24的cache介面

本課依5.24 tag核對，採`DynamicCache(config=model.config)`，forward傳`cache=cache`，從`out.cache`讀取結果。不要因為舊範例使用`past_key_values`，就把舊名稱當作當日推薦寫法；也不要傳一個框架實際沒有使用的`cache_position`，便以為絕對位置已被處理。

範例先prefill前三個token，再傳最後兩個新token，完整attention mask覆蓋5個key位置，position_ids明列`[[3,4]]`。比較完整前向後兩位置與cache路徑的logits，再核對cache長度和每層K/V形狀。query heads為4、KV heads為2，所以key head軸應反映2，而不是用4個query heads推測K形狀。

DynamicCache可能原地更新。做多條對照路徑時，每條都建立自己的新cache，不能把已增加到長度5的物件，當成原本長度3的快取重用。這種狀態污染會讓測試在不同執行順序下得到不同結果。

## 本機保存、重讀與離線邊界

`24_hf_offline_model.py`同時保存model與tokenizer，再用同一本機路徑及`local_files_only=True`重讀。比對固定輸入logits和token IDs，而不是只檢查檔案存在。程式也設定`HF_HUB_OFFLINE=1`；離線的含義是執行時不需要Hub，並不代表安裝需求不需要網路。

此流程保存config、權重和tokenizer資料，不包含optimizer、RNG與精確續訓游標。不要替現行`save_pretrained`盲加舊版`safe_serialization`必要參數；要依5.24介面使用。若切換到外部預訓練權重，還需要另外核對授權、下載大小、模型卡、模板、硬體與來源，本課預設驗收不包含那些條件。

## 練習與解析

**題目：** 回傳logits的argmax與完整路徑相同，但max_logit_error明顯變大，能否判定cache通過？

**解析：** 不能。argmax只看最大位置，可能掩蓋整個分布的偏差。先確認eval、dtype、mask、位置和是否重用被改動的cache，再定位第一個差異layer。判定標準應是事先設定的數值容差與明確案例，而不是生成句子剛好一樣。

## 參考與日期

查核日期：2026-11-24；小型config與測試IDs為原創。

- [Transformers 5.24 Llama實作](https://raw.githubusercontent.com/huggingface/transformers/v5.24.0/src/transformers/models/llama/modeling_llama.py)
- [Transformers 5.24 cache實作](https://raw.githubusercontent.com/huggingface/transformers/v5.24.0/src/transformers/cache_utils.py)
- [框架官方離線模式](https://huggingface.co/docs/transformers/en/installation#offline-mode)

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 25_hf_cache.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:25_hf_cache.py -->

