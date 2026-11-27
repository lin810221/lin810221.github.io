# OpenAI Responses的圖片與PDF輸入

用明確的內容型別傳入文件，再驗證完整回應狀態。

## 文件與圖片輸入

Responses的PDF範例使用input_file，圖像使用input_image，不能把PDF的base64字串假裝成圖片URL。PDF處理可涉及文字與頁面視覺，模型也必須支援所需輸入。檔案大小、頁數、模型與帳號能力依當日官方文件核對，不沿用其他服務的限制。

## 本課的請求

程式把合成PDF編成inline資料，使用明確模型ID、輸出token上限與 `text.format` 的JSON Schema；要求缺值可回null。`store=False` 是這個端點的設定，不可據此推論所有上傳、日誌或組織資料政策都是零保留。本課自訂2MB輸入預算，並非宣稱供應商只能收2MB。

## 回應驗收

先看status是否完成，再區分output_text與refusal，最後解析JSON並在本機驗證欄位。不能假設output第一個元素一定就是答案，也不能把截斷當作來源缺值。預設dry-run只顯示端點、schema和檔案大小；明確指定live後才會讀金鑰與上傳。

## 操作步驟

```powershell
python providers.py --provider openai --model YOUR_SUPPORTED_MODEL --pdf data/invoice.pdf
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/17.svg" target="_blank" rel="noopener" aria-label="放大OpenAI Responses的圖片與PDF輸入示意圖"><img src="assets/figures/17.svg" alt="逐列辨認PDF輸入和結構化輸出所在位置，不要把某家JSON鍵直接貼到另一家。" loading="lazy"></a><figcaption>Gemini範例使用穩定v1；模型ID由使用者明確指定。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「OpenAI Responses的圖片與PDF輸入」讀圖：逐列辨認PDF輸入和結構化輸出所在位置，不要把某家JSON鍵直接貼到另一家。本單元請再回答：PDF可以直接放進input_image的data URL嗎？</p></div>

## 自我檢查與解析

**問題：**PDF可以直接放進input_image的data URL嗎？

<details><summary>展開解析</summary><p>不應。PDF與圖片是不同內容型別，應按官方契約使用input_file或先明確渲染為影像；後者還要自行保留頁碼與座標。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab17.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab17.py -->

## 官方與原始來源

[本單元對應來源](https://developers.openai.com/api/docs/guides/file-inputs)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
