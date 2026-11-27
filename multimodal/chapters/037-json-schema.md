# JSON Schema、Pydantic與必要欄位

結構化輸出先約束形狀，再由應用程式驗證內容。

## Schema定義什麼

列出欄名、型別、必填、nullable、允許值、數值範圍與額外欄位政策。缺少欄位和欄位值為null是不同狀態；要求所有欄位存在時，也要定義沒有證據時如何表達。提供schema可降低解析歧義，但不能讓沒有來源的值變真。

## 嚴格驗證

Pydantic預設可能轉型，本課必要資料使用strict模式並拒絕額外欄位。布林值不能被當作美分整數，字串金額也先走明確的十進位解析。Python物件和JSON輸入對某些日期型別的處理可能不同，因此本課用明確字串和業務validator驗證日期。

## 不同服務的子集

供應商通常只支援JSON Schema的一部分，不能把完整本機schema原封不動當作所有服務的保證。服務端結構約束和本機驗證分開維護；本課API示範只抽兩個nullable字串，完整發票驗證仍在DocWeave應用層完成。

## 完整專案中的實作

以下節錄 `examples/contracts.py` 的 `Invoice`；請使用完整程式包，保留匯入、依賴與fixture。

```python
class Invoice(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    document_sha256:str=Field(pattern=r'^[a-f0-9]{64}$')
    invoice_no:str=Field(pattern=r'^DW-\d{4}-\d{3}$')
    invoice_date:str
    currency:Literal['USD']
    subtotal_cents:int=Field(ge=0)
    tax_cents:int=Field(ge=0)
    total_cents:int=Field(ge=0)
    evidence:dict[str,Evidence]
    @model_validator(mode='after')
    def reconcile(self):
        date.fromisoformat(self.invoice_date)
        if self.subtotal_cents+self.tax_cents!=self.total_cents:raise ValueError('Subtotal plus tax must equal total')
        required={'invoice_no','invoice_date','currency','subtotal_cents','tax_cents','total_cents'}
        if set(self.evidence)!=required:raise ValueError('Each extracted field needs evidence')
        return self
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener" aria-label="放大JSON Schema、Pydantic與必要欄位示意圖"><img src="assets/figures/13.svg" alt="逐項檢查型別、4500與225是否對成4725，以及每個欄位是否可回到來源區域。" loading="lazy"></a><figcaption>缺值保留unknown，不以猜測讓結構看起來完整。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「JSON Schema、Pydantic與必要欄位」讀圖：逐項檢查型別、4500與225是否對成4725，以及每個欄位是否可回到來源區域。本單元請再回答：模型輸出通過JSON Schema，是否表示發票號和總額一定正確？</p></div>

## 自我檢查與解析

**問題：**模型輸出通過JSON Schema，是否表示發票號和總額一定正確？

<details><summary>展開解析</summary><p>不是。Schema檢查結構與型別，來源支持、欄位歸屬、業務對帳和權限仍由其他驗證負責。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab13.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab13.py -->

## 官方與原始來源

[本單元對應來源](https://docs.pydantic.dev/latest/concepts/strict_mode/)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
