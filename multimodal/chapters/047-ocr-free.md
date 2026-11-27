# OCR-based、OCR-free與混合架構

省略獨立OCR模組，不代表省略辨識與驗證責任。

## 兩條代表路線

OCR-based方法先取得字詞與位置，再以版面或語言模型處理；LayoutLMv3是文字、影像和布局聯合表示的研究例子。OCR-free方法直接從文件影像生成結構，Donut是早期代表。這些名稱描述架構與研究脈絡，不等同目前任意產品的精度排名。

## 誤差怎麼傳遞

獨立OCR讓字串和框較容易觀察，但漏字會影響下游。端到端方法減少模組交接，卻可能更難分辨是讀錯、推理錯或格式生成錯。對特定資料可能各有優勢；應比較相同任務和來源，不把「OCR-free」當成不會識字錯誤的保證。

## 混合策略

可先用原生解析與規則基線，必要區域才交OCR或VLM，再以一致schema與引用驗收。這有助控制成本並保留可觀測性，但增加路由與版本責任。失敗時保存每層證據，避免多個模型互相覆寫後只剩一個無法解釋的值。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/16.svg" target="_blank" rel="noopener" aria-label="放大OCR-based、OCR-free與混合架構示意圖"><img src="assets/figures/16.svg" alt="沿影像patch走到視覺token與語言輸出，指出OCR文字在哪裡可作補充，以及生成仍可能幻覺。" loading="lazy"></a><figcaption>此為架構圖；不代表各供應商公開了相同內部實作。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「OCR-based、OCR-free與混合架構」讀圖：沿影像patch走到視覺token與語言輸出，指出OCR文字在哪裡可作補充，以及生成仍可能幻覺。本單元請再回答：OCR-free模型沒有獨立OCR輸出，是否就不會受到文字辨識錯誤影響？</p></div>

## 自我檢查與解析

**問題：**OCR-free模型沒有獨立OCR輸出，是否就不會受到文字辨識錯誤影響？

<details><summary>展開解析</summary><p>不會。它仍須從影像讀取資訊，只是辨識隱含在端到端模型內；字形、版面與生成錯誤仍需驗證。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab16.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab16.py -->

## 官方與原始來源

[本單元對應來源](https://arxiv.org/abs/2111.15664)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
