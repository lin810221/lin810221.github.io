# 掃描PDF、混合頁與OCR分流

先知道頁面有什麼，再選擇抽取方式。

## 空文字和空白頁不同

scan fixture把完整發票放成一張影像，原生解析會取得空文字，但人眼仍能讀出欄位。混合文件可能前幾頁是數位文字、後幾頁是掃描，甚至同一頁同時有原生標籤與影像表格。分流應細到頁面或區域，而非只看副檔名。

## 避免重複OCR

若已存在可信的文字層，直接再次OCR可能造成重複字詞與不同座標。相反地，文字層只有頁首也不能說整頁都不必OCR。正式規則可結合可見內容、文字覆蓋、字元品質與任務欄位，再用驗證集調整，不能用單一字數門檻當成通用判定。

## 主線的保守行為

DocWeave數位發票管線遇到沒有原生文字的第一頁會停止，提示改走明確OCR與覆核流程；它不會自己補值發布。另一個入口確實在影像上跑PP-OCRv6，供讀者觀察字串與區域。把OCR結果接回自動發布前，還要重新驗證表格與欄位契約。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/06.svg" target="_blank" rel="noopener" aria-label="放大掃描PDF、混合頁與OCR分流示意圖"><img src="assets/figures/06.svg" alt="辨認兩條路線的共同輸出是附座標的文字，再指出OCR多出來的辨識與品質責任。" loading="lazy"></a><figcaption>文字層可有錯誤或過期OCR，仍需抽樣視覺核對。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「掃描PDF、混合頁與OCR分流」讀圖：辨認兩條路線的共同輸出是附座標的文字，再指出OCR多出來的辨識與品質責任。本單元請再回答：為什麼掃描範例可跑OCR，主專題仍不直接自動發布掃描發票？</p></div>

## 自我檢查與解析

**問題：**為什麼掃描範例可跑OCR，主專題仍不直接自動發布掃描發票？

<details><summary>展開解析</summary><p>因為能辨識字串不等於已完成相同的表格、欄位、引用與對帳驗收。本課把這個差距明列，避免用數位模板規則假裝支援所有掃描。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab06.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab06.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/ocr/index.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
