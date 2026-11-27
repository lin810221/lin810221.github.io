# 總複習、學習路線與查核紀錄

把機制、原稿、實作和驗收證據一起帶走。

## 完成後的能力

能辨認數位與掃描來源，建立頁面座標契約，執行原生解析與真實OCR，處理基本框線表格與AcroForm，用schema、金額和區域引用驗證欄位，理解CLIP、VLM、OCR-free和MaxSim，設計可拒答的文件問答與評估，並完成可恢復的版本化交付。

## 版本與證據

查核日2026-11-27，核心為PyMuPDF 2.2、pypdf 7.2.0、Pillow 13.0.0、Pydantic 2.14.4、RapidOCR 3.10.0和ONNX Runtime 1.32.0；實測Python 3.14.10。API以當日官方文件的Responses、穩定Gemini Interactions v1和Claude Messages建構，模型ID由使用者依正式支援明確指定。

## 學習包與下一步

[學習單](study/worksheet.md)、[解析](study/answers.md)、[術語](study/glossary.md)、[來源](study/sources.md)與[版本](study/versions.json)均可保存。程式包另附原始fixture和操作手冊。付費API、大型VLM、ASR、MP4與雲端部署沒有冒稱已代跑；擴充前先寫契約、真值、反例與驗收。

需要更深入訓練可接影像辨識、Transformer與微調；需要資料交付可接SQL；需要知識助理可接RAG、搜尋與MCP。這些是跨課閱讀，本課必要主線已保留在自己的資料夾。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/32.svg" target="_blank" rel="noopener" aria-label="放大總複習、學習路線與查核紀錄示意圖"><img src="assets/figures/32.svg" alt="沿來源、模型和schema三條版本線檢查一次升級，選出需要重跑的文字、欄位、引用與恢復測試。" loading="lazy"></a><figcaption>版本以2026-11-27查核為準；大型VLM、付費API與雲端服務未代跑。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「總複習、學習路線與查核紀錄」讀圖：沿來源、模型和schema三條版本線檢查一次升級，選出需要重跑的文字、欄位、引用與恢復測試。本單元請再回答：把課程專題換成自己的文件前，最先應保留並補上的東西是什麼？</p></div>

## 自我檢查與解析

**問題：**把課程專題換成自己的文件前，最先應保留並補上的東西是什麼？

<details><summary>展開解析</summary><p>保留來源、配方、真值與反例，重新定義文件種類、語言、欄位、單位、引用、權限和失敗政策，再依新資料驗收，不能只替換檔名。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab32.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab32.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/changes.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
