# GPT與現代Decoder家族

<figure class="tf-figure"><a href="assets/figures/21-architecture-task-map.svg" target="_blank" rel="noopener"><img src="assets/figures/21-architecture-task-map.svg" alt="encoder三乘三全連接、encoderdecoder來源與目標間crossattention、decoder三乘三因果下三角並列。" loading="lazy"></a><figcaption>架構家族與常見任務。選架構時先判斷要讀完整序列、條件生成，還是依前綴續寫，再看訓練目標。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>對照架構的可見性、學習目標、常駐參數與每步工作，不以模型名稱代替能力證據。 本頁主題：GPT與現代Decoder家族。</p></div>

抓住因果語言建模的共同骨架，分辨位置表示、正規化、MLP 與注意力頭的可公開差異。

## 共同目標是條件序列機率

Decoder-only 因果 LM 依前文預測下一個 token。它可以把任務說明、示範與使用者問題放在同一個上下文，接著生成答案；核心機率仍是按序列位置分解。提示改變條件輸入，沒有直接改寫模型權重。

$$
p_\theta(x_{1:T})=\prod_{t=1}^{T}p_\theta(x_t\mid x_{<t})
$$

這個目標能支援多種文字任務，但不保證模型知道「哪一段應被當成高優先指令」，也不保證輸出事實正確。聊天格式、工具協定、拒答與任務偏好常涉及後訓練及系統設計，不能只由因果遮罩推導出來。

## 歷史架構與現代變體

GPT-2 是理解 decoder 家族的重要歷史例子；現代公開模型則可能改用 RoPE、RMSNorm、gated MLP、GQA 等元件。這些不是一個不可拆分的組合：每項都改變特定運算或表示，效益需在相應資料與預算下驗證。

| 元件 | 想處理的問題 | 不能單靠它保證什麼 |
| --- | --- | --- |
| 位置表示 | 讓模型區分順序與相對位置 | 任意長度都可靠 |
| 正規化與殘差 | 調整層內尺度及資訊路徑 | 訓練永遠穩定 |
| Gated MLP | 以可學的門控形成非線性表示 | 必然有更好推理 |
| GQA | 多個 query 頭共享部分 KV 頭 | 所有記憶體與延遲按同倍率下降 |

公開來源未披露的商用模型內部細節不能猜測。產品名稱、模型家族、特定 checkpoint 與 API 服務版本也要分開，不能用同一個品牌詞代表固定架構。

## 一個維度完整的小模型

原創配置取 hidden  `size=32` 、query  `heads=4` 、KV  `heads=2` 、head  $\mathrm{dimension}=8$ 。單筆長 6 的 query 投影可排成  $1\times 4\times 6\times 8$ ，K、V 各為  $1\times 2\times 6\times 8$ 。K、V 沒有因為模型 hidden size 是 32，就一定也保留四個頭。

若兩層 full-attention cache、 `batch=1` 、序列長 100、float32，純 KV tensor 為 \(2\times2\times1\times100\times2\times8\times4=25600\) bytes。這不含權重、暫時張量與配置器；把 KV 頭改成四個會使這部分變 51200 bytes，卻不能說整個模型記憶體也必定加倍。

## 隨機架構不等於已學會語言

以設定檔建立微型 Llama 類模型，是檢查張量、因果性、cache 與本機存取的好方法。它的隨機權重不具有大型預訓練模型的語言知識，能輸出 token ID 也不代表回答有意義。小型合成序列訓練可驗證特定規則學習，仍不能宣稱重現某個正式 LLM。

本課版本基準為 2026-11-24 查核的 PyTorch 2.15.0、Transformers 5.24.0。最新 Llama 介面使用 cache 與輸出 cache；過去的 past_key_values 是相容別名，教材應依實測介面更新。架構概念相同，不代表跨版本參數名稱永遠不變。

## 比較 family 應看完整條件

總參數量可能被 embedding 與詞表大小明顯影響；相同參數量也可能有不同層數、寬度及 KV 結構。比較模型還需要 tokenizer、訓練 token 數、資料品質、目標、上下文設定、後訓練與推論預算。若這些同時改變，單一結果不能隔離某元件的因果效果。

讀到某家族「擅長程式」時，追查它是架構、訓練資料、後訓練或評測設定的結果。沒有消融與可比條件時，保留不確定性。模型發表年份也不是效能順序的替代指標。

## 練習與解析

**題目：** 兩個 decoder 都有 100M 參數，一個詞表 1000、另一個 100000，能否斷言內部運算相同？將小模型的 RoPE 改掉後一題答對，能否稱它更會推理？

**解析：** 不能，embedding、輸出投影及其他層的配置可能差很多；還要看權重是否共享。單題成功可能是偶然或其他設定變動，需固定資料與預算、使用多樣未見題及重複實驗。公開實作可檢查的結構與尚未證明的能力主張要分開。

## 原始來源

[GPT-2 技術報告，2019](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)、[官方 Llama 文件](https://huggingface.co/docs/transformers/en/model_doc/llama)、[GQA 原論文，2023](https://arxiv.org/abs/2305.13245) 是家族與元件參考。微型尺寸與記憶體算例為原創，不涉及外部預訓練權重。


## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 24_hf_offline_model.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:24_hf_offline_model.py -->

