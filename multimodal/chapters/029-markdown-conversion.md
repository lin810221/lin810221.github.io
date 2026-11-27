# Markdown、HTML與結構保真

轉換格式要說明保留了什麼，也要看見失去了什麼。

## Markdown的用途

Markdown方便閱讀、切chunk與版本比較，但不擅長任意合併儲存格、複雜對齊與頁面定位。轉換後文字流暢，不代表原表格語意完整。若模型用Markdown回答，再把答案連回PDF時，仍需要原始節點和座標映射。

## HTML與JSON的互補

HTML可表達rowspan、colspan與較多結構，JSON可保留層級、型別和證據欄位。這些格式本身都不保證內容正確，且輸出HTML要轉義不可信文字，避免文件中的標籤或腳本成為可執行頁面。展示與資料儲存可以採不同表示。

## 轉換驗收

比較必要欄位、表格維度、合併關係、標題與引用是否可回到來源。轉換器升版時保留原PDF與預期結構，不只做全文diff。本課review頁把原生欄位、原頁PNG和疊框一起顯示，資料JSON仍是獨立產物。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/10.svg" target="_blank" rel="noopener" aria-label="放大Markdown、HTML與結構保真示意圖"><img src="assets/figures/10.svg" alt="從文件走到頁面和字詞，再找出欄位引用需要哪四個資訊；指出頁碼相同不代表來源相同。" loading="lazy"></a><figcaption>圖形、表格與欄位可增加節點型別，不要只拼接成字串。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Markdown、HTML與結構保真」讀圖：從文件走到頁面和字詞，再找出欄位引用需要哪四個資訊；指出頁碼相同不代表來源相同。本單元請再回答：文件轉成Markdown後看起來很順，是否就可刪除原PDF與座標？</p></div>

## 自我檢查與解析

**問題：**文件轉成Markdown後看起來很順，是否就可刪除原PDF與座標？

<details><summary>展開解析</summary><p>不應。Markdown可能遺失布局、合併儲存格、單位與定位，原檔和映射是查證、修復與升級驗收的重要資產。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab10.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab10.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/page.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
