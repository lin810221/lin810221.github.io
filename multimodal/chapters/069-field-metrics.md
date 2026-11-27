# 欄位Precision、Recall與整份文件成功率

明確定義一個正確欄位是什麼，再談平均分數。

## 先定義配對與正確

欄位名和值都對、來源和頁面也支持，才算符合任務的正確擷取。缺值、額外猜值與配錯欄分別影響漏失與誤報。多個重複候選要先用明確匹配規則處理，不能同一真值被多次計為成功。

## 正式定義

令 $TP,FP,FN$ 分別為正確、錯誤與漏失的欄位數：

$$
P=\frac{TP}{TP+FP},\qquad R=\frac{TP}{TP+FN},\qquad F_1=\frac{2TP}{2TP+FP+FN}.
$$

只有分母為正時才有定義。本課 $TP=8,FP=2,FN=1$ 時，$F_1=16/19$；完全沒有可評欄位時回傳未定義，不自動當滿分。微平均與每類宏平均回答不同問題，需分別標示。

## 文件級成功

一份發票的必要欄位全部通過，才算可自動交付；平均欄位高分仍可能讓每份文件都留一個關鍵錯誤。另報總額、日期、識別值等重要欄位，以及接受率、覆核量與來源支持。

## 完整專案中的實作

以下節錄 `examples/metrics.py` 的 `prf`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def prf(tp,fp,fn):
    if any(type(n) is not int or n<0 for n in (tp,fp,fn)):raise ValueError('Counts must be nonnegative integers')
    return {'precision':tp/(tp+fp) if tp+fp else None,'recall':tp/(tp+fn) if tp+fn else None,'f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None}
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/23.svg" target="_blank" rel="noopener" aria-label="放大欄位Precision、Recall與整份文件成功率示意圖"><img src="assets/figures/23.svg" alt="選一個錯誤案例，指出它會影響哪個分數，並說明為何一個平均分數無法代表整份文件可自動交付。" loading="lazy"></a><figcaption>先定義正規化、缺值、分母與文件級切分，再計算指標。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「欄位Precision、Recall與整份文件成功率」讀圖：選一個錯誤案例，指出它會影響哪個分數，並說明為何一個平均分數無法代表整份文件可自動交付。本單元請再回答：平均欄位F1很高，為何整份文件自動交付率仍可能很低？</p></div>

## 自我檢查與解析

**問題：**平均欄位F1很高，為何整份文件自動交付率仍可能很低？

<details><summary>展開解析</summary><p>因為每份文件可能各有一個必要欄位失敗。應同時量測文件級全部通過率與重要欄位，不只報欄位平均。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab23.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab23.py -->

## 官方與原始來源

[本單元對應來源](https://arxiv.org/abs/2007.00398)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
