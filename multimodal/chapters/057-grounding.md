# Grounding、bbox與跨座標驗證

把生成的定位資料轉成可以實際疊圖核對的物件。

## 模型座標不是自動可靠

有些模型輸出框、點或多邊形，但座標尺度、原點、旋轉和影像版本可能不同。先看明確文件，再驗證數值範圍與面積，轉回原頁後檢查是否真的包含答案。格式合法的四個數字仍可能落在錯頁或錯誤裁切圖。

## 幾何和文字共同驗收

以bbox取出區域內文字，核對quote，再看欄位標籤和數值是否屬於同一個對象。對圖表答案則要保留軸標、圖例與對應視覺元素；只引用圖中央空白處沒有支持作用。定位容差要依資料與渲染定義，不用任意擴大框來讓它通過。

## 顯示層責任

預覽圖若縮放，疊框也要用相同變換；CSS尺寸不是原始像素尺寸。網頁顯示可用SVG viewBox保存原座標，再縮放整個畫布。本課review頁直接疊到合成原頁，讓使用者看見引用位置，不只看到JSON數值。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/19.svg" target="_blank" rel="noopener" aria-label="放大Grounding、bbox與跨座標驗證示意圖"><img src="assets/figures/19.svg" alt="從47.25回到第一頁的區域，說明字串4725的資料單位與頁面小數金額為何不同。" loading="lazy"></a><figcaption>引用支持「來源寫什麼」，不保證來源內容本身真實。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Grounding、bbox與跨座標驗證」讀圖：從47.25回到第一頁的區域，說明字串4725的資料單位與頁面小數金額為何不同。本單元請再回答：bbox在合法範圍內而且有正面積，是否就通過grounding？</p></div>

## 自我檢查與解析

**問題：**bbox在合法範圍內而且有正面積，是否就通過grounding？

<details><summary>展開解析</summary><p>還不夠。必須核對來源版本、頁碼、座標變換，以及框內是否真的有支持答案的內容。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab03.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab03.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/matrix.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
