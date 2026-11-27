# 金額、幣別、日期與正規化

每個轉換都要保存原值，避免讓方便解析改變意思。

## 精確貨幣

本課USD使用兩位小數，先從文字用Decimal解析，再轉整數美分；拒絕負數、非有限值與超出小數位的輸入。這不是所有貨幣的通用尺度。含千分位、不同小數符號或括號負數時，應先按來源地區與欄位契約解析，不直接刪除所有標點。

## 日期的歧義

來源若是斜線日期，月日順序可能不清楚；擷取模型不能僅依偏好猜測。保存原文、解析規則與標準化結果，必要時標為歧義。文件日期、交易時間與檔案修改時間也不相同，不能用metadata補出缺少的業務日期。

## 正規化的驗收

編號可能有前導零或大小寫意義，姓名可能包含不同Unicode形式。正規化規則應按欄位決定並版本化，不能以同一個清洗函式套用所有內容。評估也要固定規則，否則系統輸出未變，分數卻因比較方式改變。

## 完整專案中的實作

以下節錄 `examples/contracts.py` 的 `cents`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def cents(raw):
    if not isinstance(raw,str):raise ValueError('Decimal text required')
    try:value=Decimal(raw)
    except InvalidOperation:raise ValueError('Invalid decimal') from None
    if not value.is_finite() or value<0 or value.as_tuple().exponent < -2:raise ValueError('Nonnegative amount with at most two decimals required')
    return int(value*100)
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener" aria-label="放大金額、幣別、日期與正規化示意圖"><img src="assets/figures/13.svg" alt="逐項檢查型別、4500與225是否對成4725，以及每個欄位是否可回到來源區域。" loading="lazy"></a><figcaption>缺值保留unknown，不以猜測讓結構看起來完整。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「金額、幣別、日期與正規化」讀圖：逐項檢查型別、4500與225是否對成4725，以及每個欄位是否可回到來源區域。本單元請再回答：把所有金額先轉float再乘100，為什麼不是穩健的貨幣解析方式？</p></div>

## 自我檢查與解析

**問題：**把所有金額先轉float再乘100，為什麼不是穩健的貨幣解析方式？

<details><summary>展開解析</summary><p>浮點近似和來源格式可能造成誤差或誤解。應先以明確地區與小數尺度解析十進位文字，再轉精確單位並保留原值。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab13.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab13.py -->

## 官方與原始來源

[本單元對應來源](https://docs.pydantic.dev/latest/concepts/models/)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
