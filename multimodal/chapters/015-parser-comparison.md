# 比較解析器而不把一致當真值

用相同來源與已知答案觀察引擎差異。

## 同一份輸入才能比較

先固定檔案雜湊、頁面範圍與版本，再比較PyMuPDF與pypdf輸出。如果先對某份PDF另存或OCR，再和原檔結果比較，就混入了不同來源的變動。比較前也要決定哪些換行、空白和字型替代屬於可接受正規化。

## 比較重要欄位與結構

除了全文是否相似，逐項檢查發票號、幣別、總額、表格列數和雙欄順序。本課確認兩個解析器都能找到47.25，但這不證明所有欄位都正確。若總額字串存在卻落在錯誤表格區域，全文包含測試仍會通過，因此還需要定位驗證。

## 如何使用不一致

將差異回到原頁檢查，判斷是字型映射、排序、掃描或解析器缺陷。可以選擇較可靠的路線或送人工覆核，但不能沒有依據就選較長字串、較高分或較新套件的結果。升級解析器時保留原本失敗的最小fixture。

## 完整專案中的實作

以下節錄 `examples/documents.py` 的 `compare_text`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def compare_text(path):
    return [page.extract_text() or '' for page in PdfReader(path).pages]
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/05.svg" target="_blank" rel="noopener" aria-label="放大比較解析器而不把一致當真值示意圖"><img src="assets/figures/05.svg" alt="比較可見畫面、文字物件和影像，指出複製文字成功仍無法證明欄位順序正確。" loading="lazy"></a><figcaption>保留原頁並以區域回查，避免把扁平字串當完整文件。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「比較解析器而不把一致當真值」讀圖：比較可見畫面、文字物件和影像，指出複製文字成功仍無法證明欄位順序正確。本單元請再回答：兩個解析器都輸出同一個錯誤總額，是否能以多數一致接受？</p></div>

## 自我檢查與解析

**問題：**兩個解析器都輸出同一個錯誤總額，是否能以多數一致接受？

<details><summary>展開解析</summary><p>不能。一致可能來自共同的來源錯誤、映射問題或相同的錯誤假設。應核對獨立真值、原頁區域與業務關係。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab05.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab05.py -->

## 官方與原始來源

[本單元對應來源](https://pypdf.readthedocs.io/en/stable/user/extract-text.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
