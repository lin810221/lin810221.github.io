# 模型revision、授權、來源與升級

套件版本、模型檔與處理配方是不同的版本軸。

## 版本軸

同一套件可能載入不同模型，同一模型可能配不同字典、前處理和解碼參數。記錄權重revision或hash、字典、引擎版本、影像變換、提示與schema，才能重建結果。只寫「用了某OCR」或「用了某VLM」不足以追查改變。

## 授權和取得方式

程式庫、模型權重、字型與資料集可能有不同條款，套件可安裝不代表所有資產都適合你的部署用途。PyMuPDF採雙授權選擇，RapidOCR模型與上游資產也需分別核對。本課自製教學fixture與SVG，不把本機OCR權重另外打進公開範例包。

## 升級驗收

保留原環境和失敗反例，用新環境比較文字、欄位、引用、拒答、延遲與恢復。模型更新可能修好某些頁、破壞另一些頁，平均分數不能取代重要欄位門檻。明確切換產物版本，避免新舊向量、schema與引用混用。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/31.svg" target="_blank" rel="noopener" aria-label="放大模型revision、授權、來源與升級示意圖"><img src="assets/figures/31.svg" alt="逐列決定是否可重用結果，指出相同文件雜湊為何不能取代授權檢查。" loading="lazy"></a><figcaption>產物雜湊是損壞偵測；不能取代可信寫入者或數位簽章。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「模型revision、授權、來源與升級」讀圖：逐列決定是否可重用結果，指出相同文件雜湊為何不能取代授權檢查。本單元請再回答：只更新Python套件但模型檔被默默替換，為何快取可能錯誤？</p></div>

## 自我檢查與解析

**問題：**只更新Python套件但模型檔被默默替換，為何快取可能錯誤？

<details><summary>展開解析</summary><p>因為結果可能已由不同權重產生，舊指紋卻看似相同。模型hash、字典和配方也應納入版本與驗收。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab31.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab31.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/changes.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
