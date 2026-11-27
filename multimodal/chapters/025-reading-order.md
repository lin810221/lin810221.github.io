# 多欄版面與閱讀順序

從空間區塊建立順序，而非只把字框由上到下排列。

## 視覺順序和內容流

雙欄文件常先讀完左欄再到右欄，但PDF內容流可能先畫右欄、後畫左欄；把所有框依垂直位置排序，也可能變成左右交錯。標題、頁首和跨欄圖片又有不同範圍。先辨認內容區塊和閱讀關係，再形成文字序列。

## 合成雙欄的規則基線

本課第二頁有明確左右欄，因此先用固定分界把字詞分組，再在各欄按行與水平位置排序。這是一個可執行、可檢查的假設，不是通用版面模型；真實頁面若有跨欄標題、直排、旁註或不規則欄寬，必須重新設計或使用版面模型。

## 驗收順序

用人工標註的段落順序比較，並檢查欄位標籤和值是否仍相鄰。文字內容完全相同而順序不同，可能讓模型把保固月份接到交付條件。保留區塊身分與原座標，讓錯誤可回到頁面，而不是只能看串接後的長字串。

## 完整專案中的實作

以下節錄 `examples/documents.py` 的 `reading_order`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def reading_order(words,split_x=None):
    if split_x is None:return sorted(words,key=lambda w:(round(w['bbox'][1]/8),w['bbox'][0]))
    return sorted(words,key=lambda w:(w['bbox'][0]>=split_x,round(w['bbox'][1]/8),w['bbox'][0]))
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/09.svg" target="_blank" rel="noopener" aria-label="放大多欄版面與閱讀順序示意圖"><img src="assets/figures/09.svg" alt="對照左右兩欄與跨欄錯誤箭頭，說明先分區再讀的前提，以及標題跨欄時要另外處理。" loading="lazy"></a><figcaption>本課雙欄規則只適用合成版型；不是通用版面模型。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「多欄版面與閱讀順序」讀圖：對照左右兩欄與跨欄錯誤箭頭，說明先分區再讀的前提，以及標題跨欄時要另外處理。本單元請再回答：為什麼按y座標排序可能把雙欄文件讀壞？</p></div>

## 自我檢查與解析

**問題：**為什麼按y座標排序可能把雙欄文件讀壞？

<details><summary>展開解析</summary><p>同一高度可能同時有左右兩欄內容，單一全頁排序會交錯兩條閱讀路線。應先分區，再依版型處理區塊內與區塊間的順序。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab09.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab09.py -->

## 官方與原始來源

[本單元對應來源](https://arxiv.org/abs/2204.08387)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
