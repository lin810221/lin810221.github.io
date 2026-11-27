# 頁面影像embedding與視覺文件檢索

保留布局訊息的表示，也需要任務和來源驗收。

## 為何用頁面影像

圖表、表格布局、顏色與空間關係可能在OCR純文字中消失，頁面視覺表示提供另一條檢索路線。ColPali等研究使用視覺語言表示來比較問題與頁面，讓某些任務減少預先OCR的依賴。這是特定研究方法，不能據此推論所有文件都不需要文字層。

## 產生表示的配方

記錄模型與revision、影像尺寸、裁切、token策略、向量型別與聚合方式。換任何一項可能改變向量空間或分數，索引需要重建或隔離版本。模型的語言、版型和字元能力也要用目標資料檢查。

## 執行範圍

本課解釋真實方法與部署條件，但數學例子使用手工小向量，不下載大型頁面模型，也不把算例稱為語意效果。要啟用真實模型，先核對模型授權、框架版本、記憶體和下載範圍，再用同一題集比較文字基線。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/22.svg" target="_blank" rel="noopener" aria-label="放大頁面影像embedding與視覺文件檢索示意圖"><img src="assets/figures/22.svg" alt="逐列找query token的最佳頁面token，說明此總分不是機率，也會受query長度影響。" loading="lazy"></a><figcaption>範例向量是手工數值；真實頁面embedding需另載入模型。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「頁面影像embedding與視覺文件檢索」讀圖：逐列找query token的最佳頁面token，說明此總分不是機率，也會受query長度影響。本單元請再回答：換了頁面模型或縮放方式，為何不宜直接沿用舊向量索引？</p></div>

## 自我檢查與解析

**問題：**換了頁面模型或縮放方式，為何不宜直接沿用舊向量索引？

<details><summary>展開解析</summary><p>表示空間與分數可能改變；模型、前處理和索引版本應一致，升級需重建或明確隔離並重新驗收。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab16.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab16.py -->

## 官方與原始來源

[本單元對應來源](https://arxiv.org/abs/2407.01449)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
