# OCR文字、全文搜尋與混合證據

先保留可重現的文字檢索基線，再增加跨模態表示。

## 文字檢索的強項

發票號、公司名、產品碼與具體關鍵字，常可用詞項或全文方法精確定位。OCR錯字會降低命中，過度正規化也可能改變識別值。檢索前保留原字串和清洗版本，讓漏找原因可回查，不把所有失敗都推給向量模型。

## 文字與視覺互補

文字檢索可能忽略圖表和版面；視覺表示可能掌握整體結構，卻未必精確讀取小字或編號。兩者可分別產生候選，再以共同文件與頁面ID融合。不同分數尺度不宜直接相加，需使用經驗證的正規化或排名融合。

## 權限與驗收

先限制可見來源，再檢索和排序；不要先取全域最高分再過濾，造成召回下降或私人內容進入模型。本課基線直接跳過其他租戶資料，測試也確認沒有可見結果。真實服務還要在儲存、快取與產物取用層維持相同政策。

## 完整專案中的實作

以下節錄 `examples/retrieval.py` 的 `lexical_search`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def lexical_search(query,rows,tenant,limit=5):
    words=set(re.findall(r'\w+',query.casefold()))
    result=[]
    for row in rows:
        if row['tenant']!=tenant:continue
        score=len(words&set(re.findall(r'\w+',row['text'].casefold())))
        if score:result.append({**row,'score':score})
    return sorted(result,key=lambda x:(-x['score'],x['id']))[:limit]
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/21.svg" target="_blank" rel="noopener" aria-label="放大OCR文字、全文搜尋與混合證據示意圖"><img src="assets/figures/21.svg" alt="沿文件、頁面到區域chunk追蹤來源與租戶標記，指出權限過濾應在排序前還是排序後。" loading="lazy"></a><figcaption>只在最後隱藏卡片，無法撤回已送進模型的私人內容。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「OCR文字、全文搜尋與混合證據」讀圖：沿文件、頁面到區域chunk追蹤來源與租戶標記，指出權限過濾應在排序前還是排序後。本單元請再回答：先全域取前五名再過濾租戶，為什麼可能既不安全也不好用？</p></div>

## 自我檢查與解析

**問題：**先全域取前五名再過濾租戶，為什麼可能既不安全也不好用？

<details><summary>展開解析</summary><p>私人候選可能已進入後續處理，而且過濾後不足五筆會降低合法召回。應在檢索或候選生成前施加正確權限。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab21.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab21.py -->

## 官方與原始來源

[本單元對應來源](https://arxiv.org/abs/2407.01449)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
