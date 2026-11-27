# 專題的反例、對帳與來源驗收

測試要攔住真實錯誤，而不是只確認程式有回傳值。

## 固定預期

核對發票號、幣別、必要欄位、表格兩列、總額與引用內容。測試直接使用已知fixture的正確數字，不只比較兩個可能共用錯誤函式的輸出。來源相同時，重跑版本與產物應一致，引用仍可回到原頁。

## 刻意破壞

總額改一分、刪除幣別證據、將金額改成布林、把引用移到空白區、換到第二頁、破壞產物檔，這些都應失敗。沒有原生文字的掃描也要停止主線，而不是回空物件卻宣告完成。鎖和頁數預算各有自己的測試。

## 網路邊界

全部32個入口的行為都在封鎖Python HTTP請求的測試下執行，包含真正的本機OCR。供應商請求只檢查形狀，不讀金鑰、不上傳。外部端點和正式資料仍需另外驗收，這份測試不把離線契約冒稱成服務效果。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/29.svg" target="_blank" rel="noopener" aria-label="放大專題的反例、對帳與來源驗收示意圖"><img src="assets/figures/29.svg" alt="從原PDF走到欄位與表格，再找review.html如何和同一份來源及manifest連接。" loading="lazy"></a><figcaption>掃描文件可跑真實OCR，但未通過相同契約前不自動發布。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「專題的反例、對帳與來源驗收」讀圖：從原PDF走到欄位與表格，再找review.html如何和同一份來源及manifest連接。本單元請再回答：為什麼要測「值正確但證據錯框」這個反例？</p></div>

## 自我檢查與解析

**問題：**為什麼要測「值正確但證據錯框」這個反例？

<details><summary>展開解析</summary><p>因為只測最終值會放過無法查證的輸出。文件AI的交付還包含正確來源與定位，必須能獨立失敗。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab29.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab29.py -->

## 官方與原始來源

[本單元對應來源](https://docs.pydantic.dev/latest/concepts/models/)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
