# 真正的PDF遮蔽與再擷取驗證

畫面看不到，和內容已移除，是兩種不同保證。

## 覆蓋不是移除

在文字上畫黑色矩形，底層字元可能仍可被複製、搜尋或解析。影像、註解、表單、附件、先前增量版本與metadata也可能保存資訊。遮蔽驗收不能只看一張預覽截圖，而要依檔案結構與使用目的檢查。

## 本課可執行示範

對合成PDF的demo電子郵件加入redaction，再apply並另存新檔，以PyMuPDF與pypdf重新抽字，確認目標文字不在輸出中。來源檔保持獨立，方便比較。此範例針對已知原生文字欄位，不是任意PDF或掃描文件的完整匿名化流程。

## 正式驗收

確認文字、影像、附件、表單、metadata與歷史增量皆符合政策，並核對遮蔽沒有破壞必要證據。真實個資去識別可能仍被其他欄位重新識別，不能把單一欄位刪除或雜湊當作全面匿名化。部署前依資料用途和組織規範定義驗收。

## 完整專案中的實作

以下節錄 `examples/documents.py` 的 `redact_demo`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def redact_demo(source,target,needle='demo@example.test'):
    if Path(source).resolve()==Path(target).resolve():raise ValueError('Preserve the source')
    with pymupdf.open(source) as doc:
        for page in doc:
            for rect in page.search_for(needle):page.add_redact_annot(rect,fill=(0,0,0))
            page.apply_redactions()
        doc.save(target,garbage=4,deflate=True)
    with pymupdf.open(target) as checked:
        if any(needle in p.get_text() for p in checked):raise ValueError('Text redaction verification failed')
    return str(target)
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/26.svg" target="_blank" rel="noopener" aria-label="放大真正的PDF遮蔽與再擷取驗證示意圖"><img src="assets/figures/26.svg" alt="比較覆蓋畫面後仍可擷取的文字，和移除文字物件後的結果；指出其他圖層與metadata仍要另驗證。" loading="lazy"></a><figcaption>本課只驗證合成PDF的指定欄位；不是任意檔案的匿名化認證。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「真正的PDF遮蔽與再擷取驗證」讀圖：比較覆蓋畫面後仍可擷取的文字，和移除文字物件後的結果；指出其他圖層與metadata仍要另驗證。本單元請再回答：黑色方塊蓋住文字，為何還要重新解析輸出PDF？</p></div>

## 自我檢查與解析

**問題：**黑色方塊蓋住文字，為何還要重新解析輸出PDF？

<details><summary>展開解析</summary><p>因為覆蓋可能只改變畫面，底層內容仍存在。應檢查真正的移除效果，且其他圖層、附件與metadata也需依範圍驗收。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab26.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab26.py -->

## 官方與原始來源

[本單元對應來源](https://pymupdf.readthedocs.io/en/latest/page.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
