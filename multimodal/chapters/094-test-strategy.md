# 離線測試、契約測試與真實服務驗收

讓每一種通過都有清楚的證據和限制。

## 核心實作

本課58項測試執行真實PDF擷取、框線表格、AcroForm、文字遮蔽、PP-OCRv6、嚴格schema、幾何、指標、檢索、WAV、GIF與DocWeave故障恢復。全部32個入口在Python HTTP被封鎖的情況下執行，驗證核心不依賴外部模型服務。

## API契約

供應商範例預設dry-run，測試請求形狀、明確live開關、停止狀態、拒答、截斷和JSON解析。這沒有使用金鑰或付費請求，所以不能宣稱已測到正式模型回答精度、帳號權限或最新配額。實際連線驗收應在受控資料與預算下另做。

## 網站與下載

網站檢查章節編號、搜尋、筆記、進度、圖解、公式和互動。下載包要解壓到乾淨目錄重跑，避免作者環境中未打包的檔案掩蓋問題。DOM與SVG預覽和真實瀏覽器版面也是不同層次，驗收紀錄分開列。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/32.svg" target="_blank" rel="noopener" aria-label="放大離線測試、契約測試與真實服務驗收示意圖"><img src="assets/figures/32.svg" alt="沿來源、模型和schema三條版本線檢查一次升級，選出需要重跑的文字、欄位、引用與恢復測試。" loading="lazy"></a><figcaption>版本以2026-11-27查核為準；大型VLM、付費API與雲端服務未代跑。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「離線測試、契約測試與真實服務驗收」讀圖：沿來源、模型和schema三條版本線檢查一次升級，選出需要重跑的文字、欄位、引用與恢復測試。本單元請再回答：離線測試檢查API JSON都通過，能否宣稱三家付費服務已端到端驗收？</p></div>

## 自我檢查與解析

**問題：**離線測試檢查API JSON都通過，能否宣稱三家付費服務已端到端驗收？

<details><summary>展開解析</summary><p>不能。那只證明本機契約與解析行為；正式請求、權限、模型可用性、費用和輸出品質仍需真實服務驗證。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab32.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab32.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/installation.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
