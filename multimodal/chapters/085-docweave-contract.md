# DocWeave專題契約與支援範圍

先寫出可以手算、可拒絕的交付目標。

## 輸入與必要欄位

專題接收本課合成數位PDF，第一頁包含唯一的發票號、日期、USD、小計、稅額和總額，以及兩筆框線商品列。保存來源hash，欄位用嚴格schema，每個必要欄位附quote與原頁框。不是任意商用發票辨識器，也不在沒有來源時猜值。

## 預期結果

發票號DW-2026-001，日期2026-11-20，小計4500美分、稅額225美分、總額4725美分。表格包含Cable與Adapter，逐列及總體金額都需通過。第二頁用於閱讀順序與檢索練習，不把它當作另一張發票。

## 失敗與人工路線

掃描頁、欄位歧義、表頭改變、金額矛盾和引用不支持會拒絕自動發布。掃描另有真實OCR入口，但接回此契約前還要做表格與證據驗收。這讓讀者能清楚區分已完成主線和下一階段要擴充的能力。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/29.svg" target="_blank" rel="noopener" aria-label="放大DocWeave專題契約與支援範圍示意圖"><img src="assets/figures/29.svg" alt="從原PDF走到欄位與表格，再找review.html如何和同一份來源及manifest連接。" loading="lazy"></a><figcaption>掃描文件可跑真實OCR，但未通過相同契約前不自動發布。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「DocWeave專題契約與支援範圍」讀圖：從原PDF走到欄位與表格，再找review.html如何和同一份來源及manifest連接。本單元請再回答：為什麼專題刻意限定USD和固定欄位，而不是宣稱支援所有發票？</p></div>

## 自我檢查與解析

**問題：**為什麼專題刻意限定USD和固定欄位，而不是宣稱支援所有發票？

<details><summary>展開解析</summary><p>這讓粒度、轉換、真值和拒絕條件可被完整驗證。擴大範圍需要新fixture、契約和測試，不能只改一段宣傳。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab29.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab29.py -->

## 官方與原始來源

[本單元對應來源](https://docs.pydantic.dev/latest/concepts/models/)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
