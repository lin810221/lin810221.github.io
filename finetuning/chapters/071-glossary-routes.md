# 術語與三條學習路線

依你的起點安排閱讀，仍保留完整工程主線。

## 從零到第一個模型

先讀策略、資料與模板，再完成手寫SFT和TRL。若梯度、張量與最佳化器不熟，跨課閱讀PyTorch與深度學習；若想深入Attention、位置資訊與KV Cache，接Transformer與LLM原理。這些是獨立課程，本課仍保留微調必要定義。

## 以LoRA工程為目標

完成監督與SFT後，讀矩陣、初始化、target與PEFT；再做成品回讀、合併與保留評估。GPU可用時才進QLoRA支線，逐項確認環境、量化與峰值，不能跳過資料與模板檢查。

## 以模型適應研究為目標

在SFT基準上進入DPO、持續預訓練、蒸餾、詞彙與遺忘。每次明確寫出改變的是資料、參數化還是目標，並控制比較條件。術語表位於下載學習包，提供定義與常見混淆；公式表則保留符號、條件與算例。

[PyTorch實作](../pytorch/index.html)、[深度學習](../deep-learning/index.html)、[Transformer與LLM原理](../transformer/index.html)、[RAG](../rag/index.html)、[MCP與工具整合](../mcp/index.html)、[LangGraph](../langgraph/index.html)提供不同角度。不要因為課程相關，就把微調工程當成只需要幾行Trainer的附錄。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener"><img src="assets/figures/24.svg" alt="術語與三條學習路線：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「術語與三條學習路線」讀圖：依圖將問題分層，選擇一個最小反例與能否推翻猜測的檢查。再回答：已會呼叫LLM API，最值得先補哪段？</p></div>

## 自我檢查與解析

**題目：**已會呼叫LLM API，最值得先補哪段？

<details><summary>展開解析</summary><p>先補資料、tokenizer模板、位移與監督遮罩，再跑CPU SFT；API參數經驗不能替代訓練張量與梯度契約。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/trl/v1.18.2/sft_trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
