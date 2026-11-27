# 合成資料、真值與最小基線

先用可以人工核對的文件建立正確答案。

## 兩頁發票的設計

第一頁包含發票號、日期、廠商、USD幣別、兩筆商品與小計稅額；第二頁為左右雙欄的交付與保固說明。另有同頁掃描PDF、旋轉PDF、影像、AcroForm、純音WAV與動畫GIF。資料都由程式產生，不使用真實客戶文件，讓每個錯誤可以安全重現。

## 真值不是模型輸出

expected檔記錄人工設計的正確欄位，不以某個OCR或VLM第一次回答作為標準。人工逐字稿也明寫是時間區間fixture，純音不是語音辨識測試。比較模型前保留來源、標註與處理版本，否則換一個輸出就可能不小心改變評分標準。

## 基線要簡單但誠實

原生文字、框線表格、正規表示式與業務規則能構成可靠的小型基線，優點是容易追查。它不是通用發票產品，也沒有跨語言或手寫保證。先驗證這條路線，再用VLM補上必要的變異，而不是一開始就失去可解釋的對照。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/02.svg" target="_blank" rel="noopener" aria-label="放大合成資料、真值與最小基線示意圖"><img src="assets/figures/02.svg" alt="沿來源雜湊、頁面與區域走到欄位，再找到引用如何回到原文件。" loading="lazy"></a><figcaption>JSON格式正確只是第一道門；內容仍須驗證。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「合成資料、真值與最小基線」讀圖：沿來源雜湊、頁面與區域走到欄位，再找到引用如何回到原文件。本單元請再回答：為什麼不能把某家模型輸出的JSON直接當成所有模型的真值？</p></div>

## 自我檢查與解析

**問題：**為什麼不能把某家模型輸出的JSON直接當成所有模型的真值？

<details><summary>展開解析</summary><p>這會把該模型的錯誤一起當成答案，產生偏差。真值應由任務契約與獨立標註形成，並保留不確定或歧義案例。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab02.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab02.py -->

## 官方與原始來源

[本單元對應來源](https://pypdf.readthedocs.io/en/stable/user/extract-text.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
