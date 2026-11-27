# 文字與視覺排名融合

以可檢查的排序整合候選，避免直接混合不同尺度。

## 排名融合的目的

文字分數、向量相似度與late interaction總分可能有不同尺度。若直接加總，某一種方法可能只因數值範圍較大而主導。RRF改用排名，讓不同方法提供相對次序，但仍要以真實題集驗證是否改善。

## RRF定義

對文件或頁面 $d$，第 $r$ 個檢索器中的名次為 $\operatorname{rank}_r(d)$，常數 $k>0$：

$$
\operatorname{RRF}(d)=\sum_r\frac{1}{k+\operatorname{rank}_r(d)}.
$$

未出現在某列表的候選不貢獻該項。本課用固定名次與明確同分排序，拒絕同一列表重複ID；這不等於已校準信心，也不保證最佳的k或候選深度。

## 融合後仍需查證

候選相關只表示值得查看，答案還要由來源支持。把同一頁不同版本或不同租戶混成一個ID，會讓融合結果錯誤；因此來源身分與權限要在融合前就一致。

## 完整專案中的實作

以下節錄 `examples/retrieval.py` 的 `fuse`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def fuse(rankings,k=60):
    if type(k) is not int or k<1:raise ValueError('Positive RRF constant required')
    scores={}
    for ranking in rankings:
        if len(ranking)!=len(set(ranking)):raise ValueError('Duplicate ids within one ranking')
        for rank,key in enumerate(ranking,1):scores[key]=scores.get(key,0)+1/(k+rank)
    return sorted(scores.items(),key=lambda x:(-x[1],x[0]))
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/22.svg" target="_blank" rel="noopener" aria-label="放大文字與視覺排名融合示意圖"><img src="assets/figures/22.svg" alt="逐列找query token的最佳頁面token，說明此總分不是機率，也會受query長度影響。" loading="lazy"></a><figcaption>範例向量是手工數值；真實頁面embedding需另載入模型。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「文字與視覺排名融合」讀圖：逐列找query token的最佳頁面token，說明此總分不是機率，也會受query長度影響。本單元請再回答：RRF排名第一的頁面，是否可以不讀來源就直接回答？</p></div>

## 自我檢查與解析

**問題：**RRF排名第一的頁面，是否可以不讀來源就直接回答？

<details><summary>展開解析</summary><p>不行。排名只提供相關候選，不證明答案存在或支持題意；仍需擷取、拒答與引用驗證。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab22.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab22.py -->

## 官方與原始來源

[本單元對應來源](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
