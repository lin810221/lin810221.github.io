# Gemini Interactions的正式文件請求

分清穩定端點、beta範例與不同世代的JSON形狀。

## 本次以穩定v1為主線

當日文件同時提供Interactions穩定v1與v1beta；本課使用穩定端點，文件內容以document區塊和MIME型別傳入，結構化輸出使用response_format。部分教學頁仍展示帶Api-Revision的beta例子，不應把那些參數無條件貼到穩定端點。舊generateContent也有不同結構，遷移時分別核對。

## 檔案和內容

inline方式適合小型一次性範例，大型或重用文件可評估Files API與處理狀態。上傳成功、文件可讀與模型完成回答是不同狀態。PDF、Office或其他格式的支援應依明確模型與服務文件核對，不能把文件清單中的格式推成所有版型都已高精度驗收。

## 輸出與保留政策

本課讀取completed互動中的model_output文字，再解析與驗證JSON，忽略非答案步驟。輸出預算放在generation_config。是否保存互動、檔案生命週期與組織資料政策要另外核對；穩定API不代表預設就是無狀態或零保留。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/17.svg" target="_blank" rel="noopener" aria-label="放大Gemini Interactions的正式文件請求示意圖"><img src="assets/figures/17.svg" alt="逐列辨認PDF輸入和結構化輸出所在位置，不要把某家JSON鍵直接貼到另一家。" loading="lazy"></a><figcaption>Gemini範例使用穩定v1；模型ID由使用者明確指定。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Gemini Interactions的正式文件請求」讀圖：逐列辨認PDF輸入和結構化輸出所在位置，不要把某家JSON鍵直接貼到另一家。本單元請再回答：為什麼不能把generateContent的generationConfig直接搬到Interactions請求？</p></div>

## 自我檢查與解析

**問題：**為什麼不能把generateContent的generationConfig直接搬到Interactions請求？

<details><summary>展開解析</summary><p>兩個API的資源與參數命名不同，還有穩定與beta版本差異。應依指定端點的正式schema建構，不只替換URL。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab18.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab18.py -->

## 官方與原始來源

[本單元對應來源](https://aistudio.google.com/docs/document-processing)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
