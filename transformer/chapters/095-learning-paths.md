# 學習路線與閱讀順序

<figure class="tf-figure"><a href="assets/figures/32-debug-decision-tree.svg" target="_blank" rel="noopener"><img src="assets/figures/32-debug-decision-tree.svg" alt="問題分成loss不下降生成異常cache不一致三條路，分別檢查shift更新、詞表解碼、位置與矩形遮罩。" loading="lazy"></a><figcaption>Transformer除錯路線。先定位資料、學習或推論哪一層失效，再選擇下一個能排除假說的測試。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>選本頁一個概念對照圖中shape、公式或除錯分支，說出下一個需要核對的條件。 本頁主題：學習路線與閱讀順序。</p></div>

## 依產物選路線，不以跳過基礎計算進度

這門課把Transformer與LLM的機制放在同一個可執行主線：文字如何變ID、ID如何變表示、attention如何聚合、目標如何產生梯度，以及前綴如何逐步生成。你不需要先有外部API帳號，也不用先下載大型權重。若目前沒有特定任務，建議按章順序讀，再用專題檢查自己是否真的理解。

每段讀完至少留下四種證據之一：一個能手算的數值、一個能列印的張量形狀、一個能被反例推翻的性質，或一份能重讀的artifact。只看完影片、記住模型名稱、執行一行而沒有查看輸出，都不足以判斷學習缺口。

## 從零完整路線

先完成第01至03章的機率、tokenizer、embedding與位置。此階段可以回答：同一文字的byte數、碼點數與token數為何不同；ID為什麼只能對應自己的詞表；位置改變怎麼進入模型。用`01_unicode_bytes.py`、`03_local_tokenizer.py`和`04_embedding_head.py`核對觀念。

接著讀第04至07章，將Q/K/V、mask、block、shifted loss與小型訓練串起來。先手算一列attention，再看SDPA；先用短序列列 $\frac{X}{Y}$ ，再啟動訓練。完成[從零訓練小型GPT](#085-tiny-project)後，應能指出每個輸出檔的用途，而不只說模型有學到。

第08至14章依序連到生成、cache、效率、架構、後訓練、評估與可靠性。最後用第15章專題整合，並把第16章當作查表與補缺工具。這條路線涵蓋全課主線；遇到數學卡住時回[必要數學推導與手算](#091-math-review)，而不是為了趕進度省略目標與分母。

## 已會PyTorch：聚焦手寫機制

如果已熟悉Tensor、Autograd與optimizer，可以快速閱讀環境和訓練迴圈，但仍要做tokenizer、head reshape、mask和shift對照。最有價值的檢查是把同一項機制寫成手算參照與框架運算，確認輸出一致，再改一個邊界條件觀察失敗。

推薦順序是`06_attention_arithmetic.py`、`07_sdpa_masks.py`、`10_shifted_loss.py`、`12_train_tiny_lm.py`，再到[KVCache專題](#086-cache-project)。你應能用圖說明past3、new2的矩形遮罩，並解釋為什麼右補齊不能一律取最後一格logits。這比單純把模型層數加大更能檢查工程理解。

## 想理解LLM推論：先正確再量測

從生成分布、prefill／decode讀到KV cache，再讀GQA、分塊softmax與服務記憶體。第一份交付是完整與cache路徑的logits對照；第二份才是分開prefill、decode、context與batch的計時報告。把容量公式的每個符號代成實際shape，避免把weights、scores和歷史KV混成一個「顯存」。

一個手算檢查是：batch1、2層、長度64、4個KV heads、head_dim8、float32，純KV為32KiB。這是預設TinyGPT規格下的張量估算，不是整個行程RAM。若想研究FlashAttention、PagedAttention或分散式服務，先讀機制與限制，再依硬體條件另做量測，不把課內CPU數值例當成GPU性能證據。

## 想用現行框架：做介面專題

完成基本shape與mask後，走[現行框架介面專題](#088-hf-project)，執行24與25號範例。它們建立隨機小Llama和本機tokenizer，讓你觀察config、輸出物件、現行`cache=`／`out.cache`以及保存重讀。這條路線不需要外部權重，也不會因此獲得預訓練聊天能力。

你應能指出手寫TinyGPT與框架Llama在位置、Norm、MLP和KV heads的差異。接著才考慮外部模型：額外核對模型卡、授權、模板、下載量與硬體。若需要的是API功能、工具呼叫和Agent產品行為，應跨讀[LLM服務與AI Agents](../llm/index.html)，不要把本課架構原理當成服務SDK操作手冊。

## 想閱讀研究：以問題帶論文

先用[張量參數與容量速查](#092-formula-sheet)與[術語表](#094-glossary)固定符號，再為每篇論文寫一張閱讀卡：原問題、改動元件、保留假設、比較預算、實驗資料與未解問題。讀RoPE時核對相對位置內積；讀GQA時追head數；讀FlashAttention時分開IO與算術；讀DPO時追policy與reference的序列分數。

實驗主張另用[公平實驗報告](#089-experiment-project)檢查。某篇研究在某個基準改善，不直接推出你的資料、硬體和版本也改善。先重建小型數值性質，再選可負擔的實驗，不需要一開始複製整個大型預訓練計畫。

## 跨課閱讀與下一階段

[PyTorch實作工程](../pytorch/index.html)補完整的訓練工程與Tensor使用；[深度學習](../deep-learning/index.html)建立反向傳播、最佳化和其他網路家族；[Embedding與表示學習](../embedding/index.html)深入向量比較、檢索表示與對比目標。本課會回顧必要知識，也保留各門課的獨立主線。

LLM微調工程仍是獨立規劃，未完成時不提供假連結；它將聚焦真實資料、LoRA／QLoRA、訓練pipeline與模型發布。本課的SFT、DPO與後訓練原理是理解那些流程的基礎，不把一個標量DPO算例稱為已完成模型對齊。

## 練習與解析

**題目：** 你下週只需要理解cache bug，能否直接跳到框架範例，略過tokenizer、位置和mask？請提出最短而完整的路線。

**解析：** 可縮短其他主題，但不能略過造成bug的契約。先確認ID與詞表，再讀QKV shape、因果／padding mask、position_id，執行17和18號對照，最後用25號核對框架狀態。交付第一個差異位置與可重現輸入，之後再補完整課程；最短路線由依賴關係決定，不由章數最少決定。

## 參考與日期

查核日期：2026-11-24；路線與驗收設計為原創。

- [Transformer原始研究](https://arxiv.org/abs/1706.03762)
- [PyTorch SDPA介面](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)
- [Transformers 5.24 Llama實作](https://raw.githubusercontent.com/huggingface/transformers/v5.24.0/src/transformers/models/llama/modeling_llama.py)
