# OpenAI、Gemini與雲端微調服務

供應商名稱相同，也可能是完全不同的平台能力。

## 查核日的平台差異

2026-11-25查核，OpenAI官方提供監督微調文件；支援模型、資格與方法應以當次模型目錄及API文件確認，不能假設任意最新模型都可微調。ChatGPT對話中的個人化設定，也不等於建立API微調權重。

Gemini API與AI Studio的官方頁面目前說明沒有可用的微調模型，並引導至Google Cloud的Gemini Enterprise Agent Platform；舊Vertex AI文件已重新導向。Google Cloud的訓練服務、區域與權限必須另查，不能把舊的AI Studio微調程式當作現行功能。

## 不替服務虛構統一端點

Claude或其他供應商能否使用特定模型調整，須按其正式方案與目錄查核。本課不提供假設所有供應商都有的通用 `fine_tune()` 端點。提示、上下文快取與檢索雖能適應行為，並非權重微調。

本課預設範例只模擬工作生命週期，不上傳資料、不發起付費工作。實際使用雲端前，依官方schema準備資料，確認支援模型與區域，記錄資料保存、工作ID及成品限制；完成服務工作後仍要獨立評估。

[OpenAI監督微調](https://developers.openai.com/api/docs/guides/supervised-fine-tuning)、[Gemini API微調狀態](https://aistudio.google.com/docs/model-tuning)、[Google Cloud監督調整](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/tuning/supervised-tuning)。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/21.svg" target="_blank" rel="noopener"><img src="assets/figures/21.svg" alt="OpenAI、Gemini與雲端微調服務：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「OpenAI、Gemini與雲端微調服務」讀圖：沿基底、模板與adapter追到manifest，列出回讀必須核對的身分。再回答：Gemini API的舊微調教學，能直接套到目前Google Cloud服務嗎？</p></div>

## 自我檢查與解析

**題目：**Gemini API的舊微調教學，能直接套到目前Google Cloud服務嗎？

<details><summary>展開解析</summary><p>不能直接套用。平台、資料格式、模型支援、權限與區域不同，應對照當日正式文件。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://aistudio.google.com/docs/model-tuning)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
