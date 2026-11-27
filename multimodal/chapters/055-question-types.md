# DocVQA的問題類型與必要證據

先判斷要找字、找關係還是跨區推理。

## 不同問題的工作量

「發票號是什麼」可能是單一區域擷取；「哪筆商品金額最高」需要表格列關係；「兩頁條款是否矛盾」需要跨頁比較；「圖中趨勢原因」可能超出來源直接支持。把題目類型和所需證據分開，才能選擇檢索、OCR、表格或VLM路線。

## 限定來源範圍

指定使用哪份文件、哪些頁面及是否允許外部知識。若來源沒有銀行帳號，答案應保留未知，不從一般發票常識補出。若需要計算，列出來源值、單位與運算；計算結果不是原文直接出現的字串，引用方式也要能說明推導。

## 最小可執行基線

本課answer_total只接受明確的英文總額題意，先檢索可見頁面，再以固定規則取Total。它刻意不回答任意問題，也不把這個功能稱為通用VLM。用這個小基線觀察答案、來源與拒答，再接更複雜模型。

## 完整專案中的實作

以下節錄 `examples/retrieval.py` 的 `answer_total`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def answer_total(document,tenant,query):
    intent=set(re.findall(r'\w+',query.casefold()))
    if 'total' not in intent or intent-{'what','is','the','invoice','total','amount','usd'}:return {'answer':None,'reason':'Question outside the bounded total-only rule'}
    hits=lexical_search(query,chunks(document,tenant),tenant)
    for hit in hits:
        match=re.search(r'(?m)^Total:\s*([0-9]+\.[0-9]{2})\s*$',hit['text'])
        if match:return {'answer':match.group(1),'page_index':hit['page_index'],'source':hit['document_sha256'],'method':'bounded regular expression over retrieved native text; no LLM'}
    return {'answer':None,'reason':'No supported evidence'}
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/19.svg" target="_blank" rel="noopener" aria-label="放大DocVQA的問題類型與必要證據示意圖"><img src="assets/figures/19.svg" alt="從47.25回到第一頁的區域，說明字串4725的資料單位與頁面小數金額為何不同。" loading="lazy"></a><figcaption>引用支持「來源寫什麼」，不保證來源內容本身真實。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「DocVQA的問題類型與必要證據」讀圖：從47.25回到第一頁的區域，說明字串4725的資料單位與頁面小數金額為何不同。本單元請再回答：來源沒有銀行帳號，但檢索到含Total的頁面，能否用總額當答案？</p></div>

## 自我檢查與解析

**問題：**來源沒有銀行帳號，但檢索到含Total的頁面，能否用總額當答案？

<details><summary>展開解析</summary><p>不能。檢索相關不代表支持題意。應先限制問題類型，找不到必要證據就拒答或回報未知。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab19.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab19.py -->

## 官方與原始來源

[本單元對應來源](https://arxiv.org/abs/2007.00398)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
