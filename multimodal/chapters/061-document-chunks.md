# 文件、頁面與區域的檢索單位

選擇粒度時同時保留上下文和定位能力。

## 三種粒度

整份文件保留脈絡但可能太長，頁面適合視覺表示和引用，區域chunk能縮小答案範圍但容易失去表頭、圖說與跨頁關係。依題目與資料選擇，也可採文件到頁面到區域的階層檢索；不要只按字數切斷一張表格。

## metadata不能丟

每個chunk保留來源hash、租戶、頁面索引、區域、處理版本及和上層節點的關係。相同文字出現在不同版本時，不能只依文字去重後讓引用指向錯頁。更新和刪除也需要知道哪些chunk由哪份來源產生。

## 主線基線

本課以每頁建立一個文字chunk，先按租戶過濾，再做簡單詞重疊排序。這不是語意embedding，也不是完整搜尋引擎；它讓權限、來源和拒答流程可以在小資料上檢查，再接真實向量與混合檢索。

## 完整專案中的實作

以下節錄 `examples/retrieval.py` 的 `chunks`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def chunks(document,tenant):
    return [{'id':document['sha256']+':'+str(p['page_index']),'document_sha256':document['sha256'],'tenant':tenant,'page_index':p['page_index'],'text':p['text'],'bbox':[0,0,p['width'],p['height']]} for p in document['pages']]
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/21.svg" target="_blank" rel="noopener" aria-label="放大文件、頁面與區域的檢索單位示意圖"><img src="assets/figures/21.svg" alt="沿文件、頁面到區域chunk追蹤來源與租戶標記，指出權限過濾應在排序前還是排序後。" loading="lazy"></a><figcaption>只在最後隱藏卡片，無法撤回已送進模型的私人內容。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「文件、頁面與區域的檢索單位」讀圖：沿文件、頁面到區域chunk追蹤來源與租戶標記，指出權限過濾應在排序前還是排序後。本單元請再回答：把頁面文字向量化後，為什麼仍要保留文件hash與頁碼？</p></div>

## 自我檢查與解析

**問題：**把頁面文字向量化後，為什麼仍要保留文件hash與頁碼？

<details><summary>展開解析</summary><p>向量只能協助比較表示，不能自行識別來源版本或提供定位。metadata是更新、刪除、授權與引用的必要資料。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab21.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab21.py -->

## 官方與原始來源

[本單元對應來源](https://arxiv.org/abs/2407.01449)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
