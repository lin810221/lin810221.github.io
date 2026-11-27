# 部署、監控、操作手冊與人工接手

把可跑的範例轉成可維護的服務，需要更多明確責任。

## 服務分層

教材網站是靜態閱讀器，可以離線或GitHub Pages提供。DocWeave是本機Python工具，真實上傳、排程、登入、佇列和多人覆核需要後端服務。私人文件、模型金鑰和產物不應放進公開教材部署目錄；展示資料和正式資料分開管理。

## 觀測指標

記錄來源完整性、解析失敗、OCR漏失、必要欄位通過、引用失敗、unknown、review、耗時、記憶體與服務usage。只觀察HTTP成功率會漏掉「程式成功但資料錯」；只看準確率又可能忽略排隊和成本。按文件類別與版本分層，避免總平均掩蓋退步。

## 操作與恢復

手冊說明鎖殘留、產物損壞、來源缺漏、模型檔缺少、API拒答與配額錯誤如何處理。備份後在新目錄讀回驗證，不只確認檔案存在。回退程式不會自動回復schema、權限或已發布資料，必須有明確版本與人工責任。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/32.svg" target="_blank" rel="noopener" aria-label="放大部署、監控、操作手冊與人工接手示意圖"><img src="assets/figures/32.svg" alt="沿來源、模型和schema三條版本線檢查一次升級，選出需要重跑的文字、欄位、引用與恢復測試。" loading="lazy"></a><figcaption>版本以2026-11-27查核為準；大型VLM、付費API與雲端服務未代跑。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「部署、監控、操作手冊與人工接手」讀圖：沿來源、模型和schema三條版本線檢查一次升級，選出需要重跑的文字、欄位、引用與恢復測試。本單元請再回答：服務HTTP成功率很高，為何文件AI仍可能無法使用？</p></div>

## 自我檢查與解析

**問題：**服務HTTP成功率很高，為何文件AI仍可能無法使用？

<details><summary>展開解析</summary><p>因為成功回應可能包含錯誤欄位、錯頁引用、過度拒答或大量人工覆核。需要資料品質、證據、資源和業務交付指標一起觀測。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab32.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab32.py -->

## 官方與原始來源

[本單元對應來源](https://docs.python.org/3.14/library/os.html#os.replace)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
