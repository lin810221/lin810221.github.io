# T5與序列到序列

<figure class="tf-figure"><a href="assets/figures/21-architecture-task-map.svg" target="_blank" rel="noopener"><img src="assets/figures/21-architecture-task-map.svg" alt="encoder三乘三全連接、encoderdecoder來源與目標間crossattention、decoder三乘三因果下三角並列。" loading="lazy"></a><figcaption>架構家族與常見任務。選架構時先判斷要讀完整序列、條件生成，還是依前綴續寫，再看訓練目標。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>對照架構的可見性、學習目標、常駐參數與每步工作，不以模型名稱代替能力證據。 本頁主題：T5與序列到序列。</p></div>

把輸入理解與輸出生成分開，追蹤 encoder、decoder self-attention 與 cross-attention 的資訊路徑。

## 兩段序列不必相同長度

翻譯、摘要與改寫都有一段來源 x 和一段目標 y。Encoder-decoder 先把來源轉成表示，decoder 再依已生成的目標與來源表示逐步產生答案。來源有十個 token，答案可以只有三個，也可以超過十個；兩邊長度不是同一個變數。

T5 將多種任務統一表示成 text-to-text，讓輸入與輸出都經過文字介面。這是任務表達的統一，不代表所有文字任務都具有相同錯誤成本，也不表示一組前綴就能讓未訓練模型執行任何任務。資料分布、目標與參數學習仍然必要。

## 三種注意力各自看什麼

Encoder self-attention 可讓來源位置互相參考；decoder self-attention 只看目前及先前目標位置；cross-attention 則以 decoder 表示作 query，來源表示作 key、value。Cross-attention 不是讓來源偷偷看到未來目標，而是讓產生答案的當前位置取用來源證據。

$$
p_\theta(y\mid x)=\prod_{t=1}^{T_y}
p_\theta(y_t\mid y_{<t},\operatorname{Enc}_\theta(x))
$$

當來源固定，encoder 表示可重用；生成時也可快取 decoder 過去的 K、V。不同模型對 cross-attention 的快取與返回欄位有不同規則，理解原理後仍需核對實際版本介面，不能把 Llama 的 self-attention cache 直接套用到所有 seq2seq 模型。

## Span corruption 與 sentinel

T5 的代表性預訓練方式會移除文字中的連續片段，以 sentinel 標記其位置，目標序列再依序重建被移除內容。這與逐個位置獨立放 MASK 的做法有不同輸出結構：目標可以比原文短，並需要分清不同缺口。

原創例：來源「小安 喜歡 紅色 的 花」，移除「紅色 的」後，擾動輸入可以抽象寫成「小安 喜歡 S0 花」，目標則為「S0 紅色 的 S1」。S0、S1 在真實 tokenizer 中需是已定義的特殊 token，而非隨意拼出看似相同的字串；具體結尾規則依資料配方。先用符號理解，再核對真實格式。

## Teacher forcing 的對齊

訓練時把正確的前一個目標 token 輸入 decoder，並預測下一個 token。假設目標答案是 A、B、EOS，decoder 輸入可為 START、A、B，三個輸出位置分別對準 A、B、EOS。START 的 ID 由模型契約決定，不能假定一定等於文字上的 BOS，或與來源第一個 token 相同。

若三個正確 token 的機率為 0.5、0.25、0.8，平均 NLL 為 \((0.6931+1.3863+0.2231)/3\approx0.7675\)。Padding 不計入目標數；若把長短答案的 padding 也算成正確輸出，指標可能被無意義位置拉高。訓練 loss 與推論時完整生成品質仍需分別評估。

## 長度、成本與截斷

在簡化 dense attention 算量中，encoder self-attention 受 \(T_x^2\) 影響，decoder self-attention 受 \(T_y^2\) 影響，cross-attention 則受 \(T_xT_y\) 影響；還有投影、MLP 與硬體成本。不能只看其中一項就推論完整延遲。

例如來源長度從 100 增到 200、目標維持 20，來源 attention 位置對數從 10000 變 40000，cross-attention 從 2000 變 4000。這是結構尺度說明，不是實機毫秒預測。來源被截斷後，模型可能根本沒看到答案依據；產生流暢摘要不代表資訊保留完整。

## 如何與 decoder-only 公平比較

先固定資料、tokenizer 或至少報告不同分詞成本、輸入可見範圍、輸出限制與訓練／推論預算。Decoder-only 可將來源與答案串接，對答案部分計算 loss；encoder-decoder 則顯式分成兩路。兩者都能研究條件生成，但路徑與成本不同，不適合只用總參數量斷言優劣。

摘要品質可分資訊覆蓋、事實一致、語句流暢與長度限制；只量字面相似可能獎勵照抄，卻漏掉扭曲來源的問題。真正交付時需保存來源與輸出，以便判讀答案是否受到輸入支持。

## 練習與解析

**題目：** Decoder 在訓練時把 A、B、EOS 原樣當輸入，並在同位置預測 A、B、EOS，可能出什麼問題？來源長度加倍是否一定讓總延遲變四倍？

**解析：** 若沒有正確位移，模型可能直接看見當前答案，學到無用複製。總延遲含多種運算、cache、kernel 與輸出長度，只有來源 self-attention 的簡化位置對數變四倍，不能推論整體。

## 原始來源

[T5 原論文，JMLR 2020](https://jmlr.org/papers/v21/20-074.html)、[官方 T5 模型文件](https://huggingface.co/docs/transformers/en/model_doc/t5) 可核對目標與介面。片段、機率及成本算例為原創，沒有宣稱已執行外部 T5 權重。
