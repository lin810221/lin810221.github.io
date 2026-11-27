# Claude Messages的PDF與結構化輸出

保留文件來源、內容區塊與停止原因的差異。

## PDF內容區塊

Messages範例以document區塊提供base64來源與 `application/pdf` MIME型別，再附任務文字。模型ID和支援能力要依官方目錄及帳號確認。本課不使用文件URL，避免把資料來源、遠端讀取和請求授權混在同一個示範。

## 結構化介面

本次使用 `output_config.format` 的JSON schema介面，較舊的頂層output_format與beta標頭屬遷移議題。服務支援的schema子集仍需本機驗證。原生citations與嚴格JSON輸出有相容性限制，不能以為各種功能開關都能同時啟用；欄位引用可另按官方建議設計流程。

## 完成與拒答

檢查stop_reason，再處理text區塊。max_tokens造成的截斷、refusal和完整end_turn是不同結果；解析JSON失敗應保留原因，而非將所有欄位置空後當作成功。本課dry-run不讀環境金鑰，live路線也不把完整憑證輸出到日誌。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/17.svg" target="_blank" rel="noopener" aria-label="放大Claude Messages的PDF與結構化輸出示意圖"><img src="assets/figures/17.svg" alt="逐列辨認PDF輸入和結構化輸出所在位置，不要把某家JSON鍵直接貼到另一家。" loading="lazy"></a><figcaption>Gemini範例使用穩定v1；模型ID由使用者明確指定。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Claude Messages的PDF與結構化輸出」讀圖：逐列辨認PDF輸入和結構化輸出所在位置，不要把某家JSON鍵直接貼到另一家。本單元請再回答：Claude結構化輸出和原生citations為何不能假設直接一起打開？</p></div>

## 自我檢查與解析

**問題：**Claude結構化輸出和原生citations為何不能假設直接一起打開？

<details><summary>展開解析</summary><p>它們的輸出結構存在相容性限制，官方文件明列衝突。應使用支援的組合或分階段流程，不能靠本機JSON解析掩蓋服務端不支援。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab18.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab18.py -->

## 官方與原始來源

[本單元對應來源](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
