# 圖文對齊與CLIP的基本想法

學習圖片與文字的對應，不等於讀懂所有細字與數量。

## 兩種編碼器

圖像編碼器和文字編碼器把成對資料轉成可比較表示，訓練時讓正配對更相近、其他配對相對遠離。CLIP是這條研究路線的代表，其原始研究年份與目前服務版本應分開理解。它提供跨模態表示方法，不是任意文件欄位抽取器。

## 相似度定義

對非零向量 $u,v$，餘弦相似度為：

$$
s(u,v)=\frac{u^\top v}{\|u\|_2\|v\|_2}.
$$

同方向可得 $1$，正交為 $0$，反方向可為 $-1$。它不是自動校準的機率；零向量在本課拒絕。圖文表示是否真的對齊，取決於訓練資料與目標任務，不是把兩個相同長度陣列放在一起就成立。

## 文件用途與限制

可用文字檢索圖片、做零樣本分類或找相似頁面，但精細金額、小字、空間關係和複雜表格未必可靠。文件檢索還要保留頁碼、區域與授權，不能因為向量接近就直接把某個數值當作答案。

## 完整專案中的實作

以下節錄 `examples/metrics.py` 的 `cosine`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def cosine(a,b):
    if not a or len(a)!=len(b) or any(not math.isfinite(x) for x in [*a,*b]):raise ValueError('Finite equal-dimensional vectors required')
    na,nb=math.sqrt(sum(x*x for x in a)),math.sqrt(sum(x*x for x in b))
    if not na or not nb:raise ValueError('Zero vector has undefined cosine')
    return sum(x*y for x,y in zip(a,b))/(na*nb)
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/15.svg" target="_blank" rel="noopener" aria-label="放大圖文對齊與CLIP的基本想法示意圖"><img src="assets/figures/15.svg" alt="找出兩個方向的正例與負例，說明batch內重複語意為何可能形成假負例。" loading="lazy"></a><figcaption>範例用手工矩陣演算損失，不冒稱訓練出CLIP。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「圖文對齊與CLIP的基本想法」讀圖：找出兩個方向的正例與負例，說明batch內重複語意為何可能形成假負例。本單元請再回答：一張發票和「invoice」向量很相似，是否代表模型已正確讀出總額？</p></div>

## 自我檢查與解析

**問題：**一張發票和「invoice」向量很相似，是否代表模型已正確讀出總額？

<details><summary>展開解析</summary><p>不是。全域語意相似和精細文字、數字、表格關係是不同能力，仍須OCR、欄位與引用驗證。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab15.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab15.py -->

## 官方與原始來源

[本單元對應來源](https://arxiv.org/abs/2103.00020)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
