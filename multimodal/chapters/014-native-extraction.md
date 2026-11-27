# 原生字詞擷取與來源座標

用真實解析器建立能回查的頁面表示。

## 同時取得文字與框

PyMuPDF的words輸出包含區域、字詞與區塊行資訊；本課保留這些資料以及未旋轉頁面尺寸。先讀原順序，再按任務決定排序，不把 `sort=True` 當作所有版型的正解。中文、直排、旋轉文字與跨欄標題都需要另外檢查。

## 生命週期與不可見差異

page物件依附於開啟的document；文件關閉後，不能繼續使用依賴其底層資源的物件。應在開啟期間轉成普通資料，再供後續管線使用。PDF可能帶隱藏OCR層，抽到的文字可能過期、重複或與可見畫面不一致；抽樣疊框核對仍然必要。

## 本課的檢查

inspect函式拒絕超出檔案與頁數預算的輸入，產生每頁的native_text旗標。這個旗標只表示存在可抽取字詞，不表示內容完整、正確或足以處理所有欄位。後續仍要分別驗證缺漏、重複、順序與引用。

## 完整專案中的實作

以下節錄 `examples/documents.py` 的 `inspect_pdf`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def inspect_pdf(path,max_pages=20,max_bytes=5_000_000):
    path=Path(path)
    with path.open('rb') as stream:raw=stream.read(max_bytes+1)
    if len(raw)>max_bytes or not raw.startswith(b'%PDF-'):raise ValueError('Not a bounded PDF input')
    with pymupdf.open(stream=raw,filetype='pdf') as doc:
        if doc.needs_pass:raise ValueError('Encrypted input requires a separate authorization workflow')
        if not 0<len(doc)<=max_pages:raise ValueError('Page budget exceeded')
        pages=[]
        for i,page in enumerate(doc):
            words=[{'bbox':list(w[:4]),'text':w[4],'block':w[5],'line':w[6]} for w in page.get_text('words',sort=False)]
            pages.append({'page_index':i,'width':page.cropbox.width,'height':page.cropbox.height,'rotation':page.rotation,'words':words,'text':page.get_text(sort=False),'native_text':bool(words)})
    return {'sha256':sha256(raw).hexdigest(),'pages':pages}
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/05.svg" target="_blank" rel="noopener" aria-label="放大原生字詞擷取與來源座標示意圖"><img src="assets/figures/05.svg" alt="比較可見畫面、文字物件和影像，指出複製文字成功仍無法證明欄位順序正確。" loading="lazy"></a><figcaption>保留原頁並以區域回查，避免把扁平字串當完整文件。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「原生字詞擷取與來源座標」讀圖：比較可見畫面、文字物件和影像，指出複製文字成功仍無法證明欄位順序正確。本單元請再回答：native_text為true，是否可以完全跳過影像核對與OCR評估？</p></div>

## 自我檢查與解析

**問題：**native_text為true，是否可以完全跳過影像核對與OCR評估？

<details><summary>展開解析</summary><p>不能。它只代表解析器取得了字詞；可能有隱藏舊OCR、錯誤映射、缺漏或順序問題。是否需要OCR應依頁面品質與任務證據判斷。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab05.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab05.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/page.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
