# 框線表格、儲存格與實際擷取

從頁面線段和字詞重建可驗證的列欄。

## 框線提供幾何線索

有框線的表格可先找水平和垂直邊界，再將字詞放進儲存格。但背景矩形、裝飾線、雙線與不完整框線都可能造成假列或漏列。引擎策略和容差要明確，本課使用 `lines_strict` 並關閉學習式layout，固定一個可對照的基線。

## 結構和內容一起看

表頭Item、Qty、Unit、Amount定義四欄的角色。Cable列的數量和單價必須仍配在同一列，不能只按文字順序把數字塞進陣列。空儲存格、跨行商品描述與欄位對齊，需要保留為結構問題，不以空白字串拼接掩蓋。

## 主線驗收

真實PyMuPDF擷取兩筆商品，程式核對表頭、逐列金額與小計。這是固定版型和USD的示範；實務若有運費、折扣、稅別與多幣別，應先擴充業務契約，再改SQL或Python。不能用總額恰好相等當成列欄全對的唯一證據。

## 完整專案中的實作

以下節錄 `examples/documents.py` 的 `line_table`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def line_table(path,page_index=0):
    with pymupdf.open(path) as doc:
        # Explicitly disable model layout: the core lab is deterministic and offline.
        finder=doc[page_index].find_tables(strategy='lines_strict',use_layout=False)
        return [{'bbox':list(t.bbox),'cells':t.extract()} for t in finder.tables]
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener" aria-label="放大框線表格、儲存格與實際擷取示意圖"><img src="assets/figures/11.svg" alt="從Cable列追蹤數量、單價與列金額，再核對小計；說明只擷取所有數字仍無法重建表格關係。" loading="lazy"></a><figcaption>主線使用明確框線；無框表、合併欄位與跨頁需另驗證。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「框線表格、儲存格與實際擷取」讀圖：從Cable列追蹤數量、單價與列金額，再核對小計；說明只擷取所有數字仍無法重建表格關係。本單元請再回答：擷取出六個正確數字，為何仍不足以證明兩筆商品列正確？</p></div>

## 自我檢查與解析

**問題：**擷取出六個正確數字，為何仍不足以證明兩筆商品列正確？

<details><summary>展開解析</summary><p>因為數字可能配到錯列或錯欄。還要保留表頭、商品關係、數量單價與列金額，再做逐列及小計對帳。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab11.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab11.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/page.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
