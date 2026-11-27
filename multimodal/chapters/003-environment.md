# 安裝當日穩定版與相容環境

最新套件與最新Python不一定能直接組成可執行環境。

## 本次可重現基準

2026-11-27查核的主線為PyMuPDF 2.2、pypdf 7.2.0、Pillow 13.0.0、Pydantic 2.14.4、RapidOCR 3.10.0與ONNX Runtime 1.32.0。Python最新主線為3.15.2，但這組ONNX Runtime沒有其對應wheel；本課採受支援分支的最新修補版Python 3.14.10，保留實際安裝失敗原因與成功環境，而不偷偷改用舊文件套件。

## 在獨立環境執行

解壓後進入examples目錄，建立虛擬環境並使用同一個Python安裝與執行。Windows不必先修改全域PATH，也不必啟用PowerShell腳本；可直接指定虛擬環境內的Python。macOS與Linux將路徑改為 `.venv/bin/python`，套件支援仍以該平台wheel與官方要求為準。

## 離線的條件

第一次安裝套件需要網路。核心fixture已打包，RapidOCR模型隨鎖版wheel提供，程式使用明確的本機路徑，找不到模型就停止，不自動換成未知下載。主線不需要API金鑰；付費服務與大型VLM另以選用路線標示。PyMuPDF有AGPL與商業授權選擇，部署前應核對實際使用方式與組織政策。

## 操作步驟

```powershell
py -3.14 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.venv\Scripts\python.exe run_lab.py --list
.venv\Scripts\python.exe lab01.py
.venv\Scripts\python.exe -m unittest test_examples -v
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/01.svg" target="_blank" rel="noopener" aria-label="放大安裝當日穩定版與相容環境示意圖"><img src="assets/figures/01.svg" alt="逐列比較文字層與影像，決定先解析還是OCR；說明同一PDF內為何仍要逐頁檢查。" loading="lazy"></a><figcaption>空的原生文字結果不代表空白頁，也不能直接補出欄位。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「安裝當日穩定版與相容環境」讀圖：逐列比較文字層與影像，決定先解析還是OCR；說明同一PDF內為何仍要逐頁檢查。本單元請再回答：為何這門課不直接沿用前一課的Python 3.15環境？</p></div>

## 自我檢查與解析

**問題：**為何這門課不直接沿用前一課的Python 3.15環境？

<details><summary>展開解析</summary><p>因為最新PyMuPDF的ONNX Runtime依賴目前沒有Python 3.15 wheel。本課使用相容的3.14.10，套件仍維持當日穩定版，並用完整測試證明可執行。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab01.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab01.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/installation.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
