# 租戶隔離、快取指紋與相同內容

相同位元組不代表相同存取權。

## 快取需要哪些資訊

來源hash、處理配方、模型revision、schema與正規化規則共同決定結果是否可重用。來源相同但前處理不同，舊結果不一定相容；模型相同但權限不同，也不能直接把另一租戶產物提供出去。效能最佳化不能移除授權邊界。

## 多層一致性

檢索、模型上下文、產物下載、引用預覽、日誌與快取都維持租戶與使用者可見性。只在UI隱藏卡片，或只在向量庫過濾而讓檔案URL公開，仍可能外洩。撤權後也要處理已保存的衍生資料與快取生命週期。

## 本課範圍

文字檢索基線先按tenant過濾；DocWeave產物只示範私人本機workspace，沒有多使用者登入服務。正式部署要將workspace隔離、檔案權限與存取驗證加上，不能因為本課有tenant欄位就宣稱整套服務已通過租戶安全驗收。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/31.svg" target="_blank" rel="noopener" aria-label="放大租戶隔離、快取指紋與相同內容示意圖"><img src="assets/figures/31.svg" alt="逐列決定是否可重用結果，指出相同文件雜湊為何不能取代授權檢查。" loading="lazy"></a><figcaption>產物雜湊是損壞偵測；不能取代可信寫入者或數位簽章。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「租戶隔離、快取指紋與相同內容」讀圖：逐列決定是否可重用結果，指出相同文件雜湊為何不能取代授權檢查。本單元請再回答：兩個租戶上傳相同hash的文件，可以直接共用公開產物URL嗎？</p></div>

## 自我檢查與解析

**問題：**兩個租戶上傳相同hash的文件，可以直接共用公開產物URL嗎？

<details><summary>展開解析</summary><p>不可以只依hash決定。內容相同不代表存取權相同；重用與提供資料都必須維持各自授權和隔離政策。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab21.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab21.py -->

## 官方與原始來源

[本單元對應來源](https://docs.python.org/3.14/library/hashlib.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
