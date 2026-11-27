# 欄位級證據與原頁區域驗證

每個重要資料值都能回到對應來源，而非只附一個頁碼。

## 證據的最小內容

保留document hash、page_index、bbox與quote。欄位的標準化值和來源字串可以不同，例如47.25轉成4725美分；轉換規則也要可解釋。引用的標籤與值要共同支持該欄位，不只引用同頁的任意相同數字。

## 檢查框內內容

本課先驗證頁碼與框在合法範圍，再取出框內字詞，確認quote確實出現。只做全頁文字包含測試會放過錯誤區域。對OCR的四邊形、斜字和旋轉頁，正式版本還要使用相同座標變換，不能直接套用未旋轉矩形假設。

## 證據的界線

引用可以支持「這份來源寫了這個內容」，卻不能證明來源沒有造假或數值符合外部制度。雜湊用於辨識來源與偵測變動，不是數位簽章。重要決策可能還需可信簽署、其他來源或人工審查。

## 完整專案中的實作

以下節錄 `examples/documents.py` 的 `validate_evidence`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def validate_evidence(document,evidence):
    p=evidence['page_index']
    if type(p) is not int or not 0<=p<len(document['pages']):raise ValueError('Unknown source page')
    page=document['pages'][p];rect=box(evidence['bbox'],page['width'],page['height'])
    words=[w for w in page['words'] if rect[0]-1<=w['bbox'][0] and rect[1]-1<=w['bbox'][1] and w['bbox'][2]<=rect[2]+1 and w['bbox'][3]<=rect[3]+1]
    text=' '.join(w['text'] for w in reading_order(words))
    squash=lambda s:re.sub(r'\s+','',s)
    if not evidence['quote'] or squash(evidence['quote']) not in squash(text):raise ValueError('Quote not present inside cited region')
    return True
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/20.svg" target="_blank" rel="noopener" aria-label="放大欄位級證據與原頁區域驗證示意圖"><img src="assets/figures/20.svg" alt="比較總額區與錯誤上方區域，檢查quote必須來自框內文字，不能只做全頁子字串搜尋。" loading="lazy"></a><figcaption>旋轉頁與OCR多邊形還需轉回同一個座標契約。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「欄位級證據與原頁區域驗證」讀圖：比較總額區與錯誤上方區域，檢查quote必須來自框內文字，不能只做全頁子字串搜尋。本單元請再回答：quote在整頁出現，為何錯框仍應驗收失敗？</p></div>

## 自我檢查與解析

**問題：**quote在整頁出現，為何錯框仍應驗收失敗？

<details><summary>展開解析</summary><p>因為引用宣稱支持答案的是指定區域。若框指到別處，就無法可靠覆核、裁切或重建證據，不能以全頁找到字串補救。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab20.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab20.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/page.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
