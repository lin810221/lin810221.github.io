# 頁數、token、費用與請求預算

把資源限制落在實際程式行為，而不是只寫在提示中。

## 多層預算

限制輸入位元組、頁數、渲染像素、裁切數、輸出token、逾時與總嘗試次數。供應商限制和本課自訂限制要分開，價格也依模型、地區、快取與處理模式不同，不在教材寫一個未查核的永久單價。

## 成本的教學模型

令 $n$ 為實際處理頁數、$v$ 為每頁估計視覺token、$t$ 為文字輸入token、$o$ 為輸出token，粗略工作量可寫為：

$$
B=nv+t+o.
$$

例如 $n=4,v=500,t=1000,o=600$，總量為 $3600$。這只是預算算例，未反映實際服務的縮放、快取、推理或定價；真正費用以usage與當日官方價格計算。

## 重試與觀測

暫時錯誤可以有限重試，非法輸入和schema不支援應先修正。把重試、超時和失敗也列入成本，並避免在日誌寫入原文件或金鑰。本課live每次只處理明確指定的文件，不自動切換供應商或大量批次上傳。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/18.svg" target="_blank" rel="noopener" aria-label="放大頁數、token、費用與請求預算示意圖"><img src="assets/figures/18.svg" alt="比較頁面視覺、文字層與自己產生影像兩條輸入，指出使用者設定解析度後仍要核對哪些限制。" loading="lazy"></a><figcaption>本課inline上限為2MB，是教材預算，不是供應商最大值。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「頁數、token、費用與請求預算」讀圖：比較頁面視覺、文字層與自己產生影像兩條輸入，指出使用者設定解析度後仍要核對哪些限制。本單元請再回答：把輸出token設小，是否就等於整個文件請求已受完整成本控制？</p></div>

## 自我檢查與解析

**問題：**把輸出token設小，是否就等於整個文件請求已受完整成本控制？

<details><summary>展開解析</summary><p>不是。還有輸入文字、頁面影像、切片、推理與重試成本，應同時限制多層預算並核對實際usage。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab18.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab18.py -->

## 官方與原始來源

[本單元對應來源](https://developers.openai.com/api/docs/guides/file-inputs)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
