# 從原PDF到欄位、表格和證據

每個階段輸出能被下一階段檢查的資料。

## 執行順序

先檢查來源和預算，建立頁面表示；再取得唯一欄位候選，解析日期、幣別與金額；建立每個候選的原文引用；由Pydantic驗證schema和業務關係；最後抽表格並做逐列及小計對帳。任一必要條件失敗都停止發布。

## 分開保存產物

source保存原始位元組，pages保存文字與區域，tables保存列欄，invoice保存標準化值與引用。這些資料有不同粒度，不將全部壓成一份難以追查的字串。review頁使用同一來源的渲染圖和框，讓人工可以直接核對。

## 擴充時的原則

新增OCR或VLM時，應輸出符合相同中間契約的候選，再走驗證。不要跳過表格與引用閘門，也不要把無法支援的文件直接當作數位模板處理。新階段的模型、參數和前處理都加入recipe，讓重跑可以辨識版本差異。

## 完整專案中的實作

以下節錄 `examples/pipeline.py` 的 `extract`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def extract(source,document):
    if not document['pages'][0]['native_text']:raise ValueError('Scanned page needs explicit OCR and review; no guessed extraction')
    text=document['pages'][0]['text'];fields={};evidence={}
    patterns={'invoice_no':r'Invoice:\s*(DW-\d{4}-\d{3})','invoice_date':r'Date:\s*(\d{4}-\d{2}-\d{2})','currency':r'Currency:\s*(USD)',
              'subtotal_cents':r'Subtotal:\s*([0-9]+\.[0-9]{2})','tax_cents':r'Tax:\s*([0-9]+\.[0-9]{2})','total_cents':r'(?m)^Total:\s*([0-9]+\.[0-9]{2})'}
    for key,pattern in patterns.items():
        matches=list(re.finditer(pattern,text))
        if len(matches)!=1:raise ValueError('Missing or ambiguous field: '+key)
        raw=matches[0].group(1);fields[key]=cents(raw) if key.endswith('_cents') else raw
        evidence[key]=evidence_for(source,0,matches[0].group(0).strip());validate_evidence(document,evidence[key])
    invoice=Invoice.model_validate({**fields,'document_sha256':document['sha256'],'evidence':evidence})
    tables=line_table(source)
    if len(tables)!=1 or tables[0]['cells'][0]!=['Item','Qty','Unit','Amount']:raise ValueError('Unsupported invoice table')
    rows=tables[0]['cells'][1:];total=0
    for product,quantity,unit,amount in rows:
        if not quantity.isdecimal() or int(quantity)<1 or int(quantity)*cents(unit)!=cents(amount):raise ValueError('Line-item reconciliation failed')
        total+=cents(amount)
    if total!=invoice.subtotal_cents:raise ValueError('Table subtotal mismatch')
    return invoice.model_dump(),tables
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/29.svg" target="_blank" rel="noopener" aria-label="放大從原PDF到欄位、表格和證據示意圖"><img src="assets/figures/29.svg" alt="從原PDF走到欄位與表格，再找review.html如何和同一份來源及manifest連接。" loading="lazy"></a><figcaption>掃描文件可跑真實OCR，但未通過相同契約前不自動發布。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「從原PDF到欄位、表格和證據」讀圖：從原PDF走到欄位與表格，再找review.html如何和同一份來源及manifest連接。本單元請再回答：加入VLM後，是否可以直接用它的JSON取代全部驗證階段？</p></div>

## 自我檢查與解析

**問題：**加入VLM後，是否可以直接用它的JSON取代全部驗證階段？

<details><summary>展開解析</summary><p>不能。VLM提供候選，不取代schema、對帳、來源和定位責任；應接到明確中間契約，再通過同樣閘門。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab29.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab29.py -->

## 官方與原始來源

[本單元對應來源](https://docs.pydantic.dev/latest/concepts/models/)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
