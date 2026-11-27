# 套件相容性、鎖版與CPU部署

記錄真正可安裝的組合，而不是只列一排最新數字。

## 本次相容性證據

PyMuPDF 2.2引入或整合多個layout依賴，本次解析到ONNX Runtime 1.32.0；其wheel沒有Python 3.15 ABI，因此3.15.2安裝無法成立。改用Python 3.14.10後，當日穩定PDF與OCR套件可實際執行。這是相容性選擇，不是把舊版本當最新。

## 鎖定與重建

requirements列直接依賴，lock列本次完整解析版本。不同作業系統與處理器仍可能有不同wheel可用性；升級先建立新環境重跑固定fixture與真實OCR，再更新版本紀錄。不要刪掉版本限制或忽略安裝錯誤後宣稱完成。

## 啟動檢查

列出Python、套件、推論provider和模型hash，確認使用預期CPU環境。首次安裝需要網路，執行時不自動替換模型。若要GPU、容器或雲端，另核對驅動、映像、資源、授權和目標環境驗收；本機Windows結果不等於各平台都已測過。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/31.svg" target="_blank" rel="noopener" aria-label="放大套件相容性、鎖版與CPU部署示意圖"><img src="assets/figures/31.svg" alt="逐列決定是否可重用結果，指出相同文件雜湊為何不能取代授權檢查。" loading="lazy"></a><figcaption>產物雜湊是損壞偵測；不能取代可信寫入者或數位簽章。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「套件相容性、鎖版與CPU部署」讀圖：逐列決定是否可重用結果，指出相同文件雜湊為何不能取代授權檢查。本單元請再回答：版本清單每個項目都最新，為何仍可能完全無法安裝？</p></div>

## 自我檢查與解析

**問題：**版本清單每個項目都最新，為何仍可能完全無法安裝？

<details><summary>展開解析</summary><p>因為依賴與Python ABI、作業系統和硬體的可用wheel要同時相容。應記錄實際解析和執行成功的組合，而不是只比較版本號。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab31.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab31.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/installation.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
